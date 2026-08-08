import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from graphoath.custody.ledger import Ledger
from graphoath.custody.receipt import CustodyReceipt

class MemoryRecallResult(BaseModel):
    repeat_incident_detected: bool
    occurrences_in_30d: int
    escalated_priority: str  # MEDIUM, HIGH_RECURRING
    previous_receipt_id: Optional[str] = None
    previous_incident_urn: Optional[str] = None
    memory_insight: str

class FunctionalMemoryFlywheel:
    """
    Functional Memory Recall Flywheel:
    Queries historical custody receipts over a 30-day lookback window for target dataset URN.
    Detects recurring patterns and automatically escalates priority to HIGH_RECURRING.
    """
    def __init__(self, ledger: Optional[Ledger] = None, lookback_days: int = 30):
        self.ledger = ledger or Ledger()
        self.lookback_seconds = lookback_days * 86400

    def recall_memory(self, target_urn: str) -> MemoryRecallResult:
        now = time.time()
        all_rcpts = self.ledger.get_all_receipts()
        
        matches: List[CustodyReceipt] = []
        for rcpt in all_rcpts:
            if getattr(rcpt, "target_urn", None) == target_urn:
                rcpt_time = getattr(rcpt, "created_at_ms", 0) / 1000.0 if getattr(rcpt, "created_at_ms", 0) else now
                if now - rcpt_time <= self.lookback_seconds or rcpt_time == now:
                    matches.append(rcpt)

        count = len(matches)
        repeat = count > 1

        if repeat:
            priority = "HIGH_RECURRING"
            prev_rcpt = matches[-2] if len(matches) >= 2 else matches[0]
            prev_id = getattr(prev_rcpt, "receipt_id", "rcpt_prev_001")
            prev_inc = getattr(prev_rcpt, "action_type", "urn:li:incident:prev_001")
            insight = (
                f"RECURRING PATTERN: {count}nd schema-breaking modification / incident on {target_urn} "
                f"within 30 days. Prior receipt: {prev_id}."
            )
        else:
            priority = "MEDIUM"
            prev_id = None
            prev_inc = None
            insight = f"FIRST OCCURRENCE: Single incident recorded on {target_urn} within 30-day window."

        return MemoryRecallResult(
            repeat_incident_detected=repeat,
            occurrences_in_30d=count,
            escalated_priority=priority,
            previous_receipt_id=prev_id,
            previous_incident_urn=prev_inc,
            memory_insight=insight
        )
