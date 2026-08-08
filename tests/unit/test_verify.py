import pytest
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.custody.verify import verify_ledger_chain

def test_verify_ledger_chain_healthy():
    ledger = Ledger()
    r1 = CustodyReceipt(receipt_id="r1", action_type="act", target_urn="urn:1", evidence_payload=[], claims_payload={})
    ledger.append_custody_receipt(r1)

    res = verify_ledger_chain(ledger)
    assert res["status"] == "HEALTHY"
    assert res["is_valid"] is True
    assert res["verified_receipt_count"] == 1
    assert "head_ledger_hash" in res

def test_verify_ledger_chain_corrupted():
    ledger = Ledger()
    r1 = CustodyReceipt(receipt_id="r1", action_type="act", target_urn="urn:1", evidence_payload=[], claims_payload={})
    ledger.append_custody_receipt(r1)
    
    # Tamper with current hash
    ledger._memory_custody_ledger[0].current_hash = "corrupted_hash"

    res = verify_ledger_chain(ledger)
    assert res["status"] == "CORRUPTED"
    assert res["is_valid"] is False
    assert res["break_at_receipt_id"] == "r1"
