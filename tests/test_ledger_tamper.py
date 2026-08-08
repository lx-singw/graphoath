import pytest
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.custody.verify import verify_ledger_integrity

@pytest.mark.asyncio
async def test_ledger_tamper_detection_10_receipts():
    Ledger.clear_memory()
    ledger = Ledger()
    
    # 1. Insert 10 valid receipts
    for i in range(1, 11):
        rcpt = CustodyReceipt(
            receipt_id=f"rcpt_{i}",
            action_type="raiseIncident",
            target_urn=f"urn:li:dataset:table_{i}",
            evidence_payload=[{"urn": f"urn:li:dataset:table_{i}"}],
            claims_payload={"index": i},
            sequence_number=i
        )
        ledger.append_custody_receipt(rcpt)

    # Assert verify_ledger_integrity() returns is_valid=True
    res = await verify_ledger_integrity(ledger=ledger)
    assert res["is_valid"] is True
    assert res["status"] == "VALID"
    assert res["total_receipts_verified"] == 10
    assert res["tampered_receipt_id"] is None

    # 2. Directly tamper with payload of receipt #5
    ledger._memory_custody_ledger[4].current_hash = "tampered_hash_00000000000000000000000000000000000000000000000000"

    res_tampered = await verify_ledger_integrity(ledger=ledger)
    assert res_tampered["is_valid"] is False
    assert res_tampered["status"] == "CORRUPTED"
    assert res_tampered["tampered_receipt_id"] == "rcpt_5"

def test_prevent_receipt_mutation_simulation():
    Ledger.clear_memory()
    ledger = Ledger()
    rcpt = CustodyReceipt(
        receipt_id="rcpt_immutable_1",
        action_type="addTag",
        target_urn="urn:li:dataset:immutable",
        evidence_payload=[],
        claims_payload={}
    )
    ledger.append_custody_receipt(rcpt)
    
    # Verify hash chain is initialised
    is_intact, count, _ = ledger.verify_chain()
    assert is_intact is True
    assert count == 1
