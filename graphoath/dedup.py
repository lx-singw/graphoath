"""
GraphOath Incident De-Duplication & Alert Grouping Module.

Prevents alert fatigue during cascading failures by grouping downstream impacts by root-cause dataset URN.
"""

import time
from typing import List, Dict, Any, Tuple

class IncidentDeduplicator:
    """
    Tracks active incidents in a 15-minute sliding window to prevent duplicate incident creation.
    """
    def __init__(self, window_seconds: int = 900):
        self.window_seconds = window_seconds
        self.active_incidents: Dict[str, Dict[str, Any]] = {}

    def process_incident_claim(
        self,
        source_urn: str,
        downstream_urns: List[str]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Returns:
            (action_type: "CREATE" | "UPDATE", incident_id: str, payload: dict)
        """
        now = time.time()
        
        # Check if active incident exists for source_urn within window
        if source_urn in self.active_incidents:
            entry = self.active_incidents[source_urn]
            if now - entry["timestamp"] < self.window_seconds:
                # Merge new downstream URNs into existing incident
                existing_urns = set(entry["downstream_urns"])
                existing_urns.update(downstream_urns)
                entry["downstream_urns"] = list(existing_urns)
                entry["timestamp"] = now
                entry["update_count"] += 1
                
                print(f"[GraphOath Dedup] Merged downstream impact into existing incident '{entry['incident_id']}'. Total updates: {entry['update_count']}")
                return "UPDATE", entry["incident_id"], entry
                
        # Create new incident entry
        incident_id = f"inc_{int(now)}"
        new_entry = {
            "incident_id": incident_id,
            "source_urn": source_urn,
            "downstream_urns": downstream_urns,
            "timestamp": now,
            "update_count": 1
        }
        self.active_incidents[source_urn] = new_entry
        print(f"[GraphOath Dedup] Created new root-cause incident '{incident_id}' for URN '{source_urn}'.")
        return "CREATE", incident_id, new_entry

if __name__ == "__main__":
    deduper = IncidentDeduplicator()
    src = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    
    # 1. First event creates incident
    act1, inc_id1, p1 = deduper.process_incident_claim(src, ["urn:li:dataset:downstream_1"])
    assert act1 == "CREATE"
    
    # 2. Second event within 15 min merges into existing incident
    act2, inc_id2, p2 = deduper.process_incident_claim(src, ["urn:li:dataset:downstream_2"])
    assert act2 == "UPDATE"
    assert inc_id1 == inc_id2
    assert len(p2["downstream_urns"]) == 2
