import pytest
from graphoath.custody.receipt import CustodyReceipt
from graphoath.ops.backup import WORMBackupStreamer

def test_worm_backup_streamer(tmp_path):
    streamer = WORMBackupStreamer()
    streamer.local_archive_dir = str(tmp_path)

    r = CustodyReceipt(
        receipt_id="rcpt_worm_001",
        action_type="raiseIncident",
        target_urn="urn:li:dataset:target",
        evidence_payload=[],
        claims_payload={},
        sequence_number=1
    )

    res = streamer.backup_receipt(r)
    assert res["status"] == "MIRRORED_TO_WORM"
    assert res["object_lock_mode"] == "COMPLIANCE"

    restored = streamer.restore_from_archive()
    assert len(restored) == 1
    assert restored[0]["receipt_id"] == "rcpt_worm_001"
