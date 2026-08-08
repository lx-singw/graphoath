import pytest
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.custody.drift import EvidenceDriftEngine

def test_evidence_drift_detection_ownership_transfer():
    Ledger.clear_memory()
    receipt = CustodyReceipt(
        receipt_id="rcpt_drift_101",
        action_type="deprecateDataset",
        target_urn="urn:li:dataset:(snowflake,prod.stg_orders)",
        evidence_payload=[
            {"urn": "urn:li:dataset:(snowflake,prod.stg_orders)", "owner": "priya_ramaswamy"}
        ],
        claims_payload={}
    )
    ledger = Ledger()
    ledger.append_custody_receipt(receipt)

    engine = EvidenceDriftEngine()
    
    # Simulate live metadata change (ownership transfer to marcus_webb)
    live_override = {
        "urn:li:dataset:(snowflake,prod.stg_orders)": {"owner": "marcus_webb"}
    }
    
    report = engine.verify_drift(receipt, live_evidence_override=live_override)
    assert report.evidence_drift_status == "CITATION_DRIFT_DETECTED"
    assert len(report.drift_details) == 1
    assert report.drift_details[0].drift_type == "OWNERSHIP_TRANSFER"
    assert report.drift_details[0].cited_fact == "owner: priya_ramaswamy"
    assert report.drift_details[0].live_fact == "owner: marcus_webb"
