import pytest
from graphoath.custody.receipt import CustodyReceipt, GENESIS_HASH
from graphoath.custody.ledger import Ledger

def test_ledger_append_and_chain():
    ledger = Ledger()
    
    r1 = CustodyReceipt(
        receipt_id="rcpt_001",
        action_type="raiseIncident",
        target_urn="urn:li:dataset:prod",
        evidence_payload=[],
        claims_payload={}
    )
    r1_appended = ledger.append_custody_receipt(r1)
    assert r1_appended.previous_hash == GENESIS_HASH

    r2 = CustodyReceipt(
        receipt_id="rcpt_002",
        action_type="addTag",
        target_urn="urn:li:dataset:prod",
        evidence_payload=[],
        claims_payload={}
    )
    r2_appended = ledger.append_custody_receipt(r2)
    assert r2_appended.previous_hash == r1_appended.current_hash

    is_intact, count, break_id = ledger.verify_chain()
    assert is_intact is True
    assert count == 2
    assert break_id is None

def test_ledger_tamper_detection():
    ledger = Ledger()
    r1 = CustodyReceipt(receipt_id="r1", action_type="act1", target_urn="urn:1", evidence_payload=[], claims_payload={})
    r2 = CustodyReceipt(receipt_id="r2", action_type="act2", target_urn="urn:2", evidence_payload=[], claims_payload={})
    
    ledger.append_custody_receipt(r1)
    ledger.append_custody_receipt(r2)

    # Tamper with first receipt current_hash
    ledger._memory_custody_ledger[0].current_hash = "tampered_hash_00000000000000000000000000000000000000000000000000"

    is_intact, count, break_id = ledger.verify_chain()
    assert is_intact is False
    assert break_id == "r1"
