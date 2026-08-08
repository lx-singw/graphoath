import pytest
import time
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.ops.memory import FunctionalMemoryFlywheel

def test_functional_memory_recall_repeat_incident():
    Ledger.clear_memory()
    target_urn = "urn:li:dataset:(snowflake,prod.orders)"
    ledger = Ledger()

    # 1. Populate receipt from 5 days ago
    r1 = CustodyReceipt(
        receipt_id="rcpt_prev_30d_01",
        action_type="raiseIncident",
        target_urn=target_urn,
        evidence_payload=[],
        claims_payload={},
        created_at_ms=int((time.time() - 5 * 86400) * 1000)
    )
    ledger.append_custody_receipt(r1)

    # 2. Append new incident receipt today
    r2 = CustodyReceipt(
        receipt_id="rcpt_today_02",
        action_type="raiseIncident",
        target_urn=target_urn,
        evidence_payload=[],
        claims_payload={},
        created_at_ms=int(time.time() * 1000)
    )
    ledger.append_custody_receipt(r2)

    # 3. Recall memory flywheel
    flywheel = FunctionalMemoryFlywheel(ledger=ledger)
    result = flywheel.recall_memory(target_urn)

    assert result.repeat_incident_detected is True
    assert result.occurrences_in_30d == 2
    assert result.escalated_priority == "HIGH_RECURRING"
    assert "RECURRING PATTERN" in result.memory_insight
