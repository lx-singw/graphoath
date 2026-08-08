import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

GENESIS_SEED = "GENESIS_BLOCK_GRAPHOATH_2026"
GENESIS_HASH = hashlib.sha256(GENESIS_SEED.encode("utf-8")).hexdigest()

@dataclass
class CustodyReceipt:
    receipt_id: str
    action_type: str
    target_urn: str
    evidence_payload: List[Dict[str, Any]]
    claims_payload: Dict[str, Any]
    agent_id: str = "deposition-v1"
    spiffe_id: str = "spiffe://graphoath.io/agent/deposition-v1"
    svid_serial: str = "svid-serial-0001"
    gate_decision: str = "APPROVED"
    confidence_score: float = 1.0
    sequence_number: int = 1
    previous_hash: str = GENESIS_HASH
    created_at_ms: int = field(default_factory=lambda: int(time.time() * 1000))
    current_hash: str = ""

    def __post_init__(self):
        if not self.current_hash:
            self.current_hash = self.compute_hash()

    def compute_payload_hash(self) -> str:
        """Computes deterministic SHA-256 hash of evidence + claims payload."""
        payload_data = {
            "target_urn": self.target_urn,
            "evidence": self.evidence_payload,
            "claims": self.claims_payload,
            "decision": self.gate_decision,
            "confidence": self.confidence_score
        }
        canonical_json = json.dumps(payload_data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def compute_hash(self) -> str:
        """
        Computes Merkle-like hash chain:
        H_n = SHA256(H_{n-1} || ReceiptID || Action || Timestamp || PayloadHash || SPIFFE_ID)
        """
        payload_hash = self.compute_payload_hash()
        chained_str = (
            f"{self.previous_hash}"
            f"||{self.receipt_id}"
            f"||{self.action_type}"
            f"||{self.created_at_ms}"
            f"||{payload_hash}"
            f"||{self.spiffe_id}"
        )
        return hashlib.sha256(chained_str.encode('utf-8')).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "sequence_number": self.sequence_number,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
            "agent_id": self.agent_id,
            "spiffe_id": self.spiffe_id,
            "svid_serial": self.svid_serial,
            "action_type": self.action_type,
            "target_urn": self.target_urn,
            "evidence_payload": self.evidence_payload,
            "claims_payload": self.claims_payload,
            "gate_decision": self.gate_decision,
            "confidence_score": self.confidence_score,
            "created_at_ms": self.created_at_ms
        }

@dataclass
class Receipt:
    """Legacy/Compatibility Receipt dataclass."""
    receipt_id: str
    module: str
    created_at: str
    trigger_info: Dict[str, Any]
    claim: str
    evidence: List[Dict[str, Any]]
    action_taken: Dict[str, Any]
    prev_hash: str
    confidence: str = "high"
    prior_receipts: List[str] = field(default_factory=list)
    memory_note: Optional[str] = None
    hash: str = ""

    def __post_init__(self):
        if not self.hash:
            self.hash = self.compute_hash()

    def to_canonical_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "module": self.module,
            "created_at": self.created_at,
            "trigger": self.trigger_info,
            "claim": self.claim,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "action_taken": self.action_taken,
            "prior_receipts": self.prior_receipts,
            "memory_note": self.memory_note,
        }

    def compute_hash(self) -> str:
        canonical_json = json.dumps(
            self.to_canonical_dict(),
            sort_keys=True,
            separators=(',', ':')
        )
        payload = self.prev_hash + canonical_json
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()

