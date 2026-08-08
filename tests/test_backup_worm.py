import pytest
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.ops.backup import MinIOBackupEngine

@pytest.mark.asyncio
async def test_mirror_receipt_and_compliance_lock(tmp_path):
    engine = MinIOBackupEngine()
    engine.local_archive_dir = str(tmp_path)

    rcpt = CustodyReceipt(
        receipt_id="rcpt_worm_100",
        action_type="raiseIncident",
        target_urn="urn:li:dataset:worm_test",
        evidence_payload=[],
        claims_payload={},
        sequence_number=1
    )

    res = await engine.mirror_receipt(rcpt)
    assert res["status"] == "MIRRORED_TO_WORM"
    assert res["object_lock_mode"] == "COMPLIANCE"
    assert res["retention_years"] == 7

@pytest.mark.asyncio
async def test_disaster_recovery_reconstruct(tmp_path):
    engine = MinIOBackupEngine()
    engine.local_archive_dir = str(tmp_path)

    # 1. Mirror 3 receipts
    for i in range(1, 4):
        rcpt = CustodyReceipt(
            receipt_id=f"rcpt_dr_{i}",
            action_type="raiseIncident",
            target_urn=f"urn:li:dataset:table_{i}",
            evidence_payload=[],
            claims_payload={},
            sequence_number=i
        )
        await engine.mirror_receipt(rcpt)

    # 2. Reconstruct into clean ledger
    clean_ledger = Ledger()
    res = await engine.disaster_recovery_reconstruct(ledger=clean_ledger)
    assert res["status"] == "RECONSTRUCTED_AND_VERIFIED"
    assert res["reconstructed_count"] == 3
    assert res["chain_is_valid"] is True
