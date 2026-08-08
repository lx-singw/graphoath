import pytest
from graphoath.custody.receipt import CustodyReceipt, Receipt, GENESIS_HASH

def test_custody_receipt_hash_chain():
    r1 = CustodyReceipt(
        receipt_id="rcpt_001",
        action_type="raiseIncident",
        target_urn="urn:li:dataset:snowflake_orders",
        evidence_payload=[{"urn": "urn:li:dataset:orders"}],
        claims_payload={"statement": "Field removed"},
        sequence_number=1,
        previous_hash=GENESIS_HASH
    )
    assert r1.sequence_number == 1
    assert r1.previous_hash == GENESIS_HASH
    assert len(r1.current_hash) == 64

    r2 = CustodyReceipt(
        receipt_id="rcpt_002",
        action_type="addTag",
        target_urn="urn:li:dataset:snowflake_orders",
        evidence_payload=[],
        claims_payload={},
        sequence_number=2,
        previous_hash=r1.current_hash
    )
    assert r2.previous_hash == r1.current_hash
    assert r2.current_hash != r1.current_hash

def test_custody_receipt_payload_hash_consistency():
    r1 = CustodyReceipt(
        receipt_id="rcpt_001",
        action_type="raiseIncident",
        target_urn="urn:li:dataset:target",
        evidence_payload=[{"a": 1}],
        claims_payload={"b": 2}
    )
    h1 = r1.compute_payload_hash()
    h2 = r1.compute_payload_hash()
    assert h1 == h2
