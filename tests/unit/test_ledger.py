import pytest
from graphoath.custody.receipt import Receipt, GENESIS_HASH
from graphoath.custody.ledger import Ledger

def test_receipt_hash_calculation():
    r = Receipt(
        receipt_id="rcpt_001",
        module="deposition",
        created_at="2026-08-05T14:32:07Z",
        trigger_info={"event": "field_removed"},
        claim="Field customer_region removed",
        evidence=[],
        action_taken={"type": "raise_incident"},
        prev_hash=GENESIS_HASH
    )
    assert len(r.hash) == 64
    assert r.compute_hash() == r.hash

def test_ledger_hash_chain():
    ledger = Ledger()
    r1 = Receipt(
        receipt_id="rcpt_001",
        module="deposition",
        created_at="2026-08-05T14:32:07Z",
        trigger_info={"event": "field_removed"},
        claim="Field customer_region removed",
        evidence=[],
        action_taken={"type": "raise_incident"},
        prev_hash=""
    )
    recorded1 = ledger.append_receipt(r1)
    assert recorded1.prev_hash == GENESIS_HASH

    r2 = Receipt(
        receipt_id="rcpt_002",
        module="deposition",
        created_at="2026-08-05T14:33:07Z",
        trigger_info={"event": "field_removed"},
        claim="Second field removed",
        evidence=[],
        action_taken={"type": "raise_incident"},
        prev_hash=""
    )
    recorded2 = ledger.append_receipt(r2)
    assert recorded2.prev_hash == recorded1.hash

    is_intact, checked, break_id = ledger.verify_chain()
    assert is_intact is True
    assert checked == 2
    assert break_id is None
