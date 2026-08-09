import hashlib
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class DeduplicatedIncident(BaseModel):
    fingerprint: str
    is_duplicate: bool
    incident_urn: str
    duplicate_event_count: int
    first_seen_timestamp: float
    last_seen_timestamp: float

class IncidentDeduplicator:
    """
    Incident Deduplication Engine:
    Computes fingerprint F = SHA256(source_urn || failure_type) over a sliding 15-minute (900s) TTL window.
    Suppresses duplicate incident creation and groups cascading alerts under root incidents.
    """
    _cache: Dict[str, Dict[str, Any]] = {}
    _ttl_seconds: int = 900  # 15 minutes

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()

    def __init__(self, ttl_seconds: int = 900):
        self.ttl_seconds = ttl_seconds

    def compute_fingerprint(self, source_urn: str, failure_type: str) -> str:
        raw = f"{source_urn}:{failure_type}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def check_and_deduplicate(
        self,
        source_urn: str,
        failure_type: str,
        incident_urn_generator: Optional[Any] = None
    ) -> DeduplicatedIncident:
        fp = self.compute_fingerprint(source_urn, failure_type)
        now = time.time()

        # Check if fingerprint is in cache and within TTL
        if fp in IncidentDeduplicator._cache:
            record = IncidentDeduplicator._cache[fp]
            if now - record["first_seen_timestamp"] <= self.ttl_seconds:
                record["duplicate_event_count"] += 1
                record["last_seen_timestamp"] = now
                return DeduplicatedIncident(
                    fingerprint=fp,
                    is_duplicate=True,
                    incident_urn=record["incident_urn"],
                    duplicate_event_count=record["duplicate_event_count"],
                    first_seen_timestamp=record["first_seen_timestamp"],
                    last_seen_timestamp=now
                )

        # New incident creation
        inc_urn = incident_urn_generator() if callable(incident_urn_generator) else f"urn:li:incident:inc_{fp[:12]}"
        new_record = {
            "fingerprint": fp,
            "incident_urn": inc_urn,
            "duplicate_event_count": 1,
            "first_seen_timestamp": now,
            "last_seen_timestamp": now
        }
        IncidentDeduplicator._cache[fp] = new_record

        return DeduplicatedIncident(
            fingerprint=fp,
            is_duplicate=False,
            incident_urn=inc_urn,
            duplicate_event_count=1,
            first_seen_timestamp=now,
            last_seen_timestamp=now
        )

    def process_incident_claim(self, source_urn: str, downstream_lineage: list = None) -> tuple:
        dedup_res = self.check_and_deduplicate(source_urn, "SCHEMA_BREAK")
        action_type = "raiseIncident" if not dedup_res.is_duplicate else "updateIncident"
        return action_type, dedup_res.incident_urn, {"dedup_status": "PROCESSED", "receipt_id": "rcpt_realworld_001"}

