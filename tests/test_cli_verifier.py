import json
import pytest
from examples.verify_receipt_chain import verify_exported_receipt_chain

def test_cli_verifier_valid_chain():
    receipts = [
        {
            "sequence_number": 1,
            "receipt_id": "rcpt_0001",
            "agent_id": "agent_1",
            "action_type": "raiseIncident",
            "target_urn": "urn:li:dataset:prod_orders",
            "status": "APPROVED",
            "previous_hash": "0" * 64,
            "hash": "a188d82fb6071b25a7a25dd5072d0fed8a89e0dab834a12d916e4e37c77b238e"
        }
    ]
    is_valid, msg, broken_idx = verify_exported_receipt_chain(receipts)
    assert is_valid is True
    assert broken_idx == -1
    assert "[VALID]" in msg

def test_cli_verifier_corrupted_prev_hash_chain():
    receipts = [
        {
            "sequence_number": 1,
            "receipt_id": "rcpt_0001",
            "hash": "hash_1",
            "previous_hash": "0" * 64
        },
        {
            "sequence_number": 2,
            "receipt_id": "rcpt_0002",
            "hash": "hash_2",
            "previous_hash": "WRONG_BROKEN_PREV_HASH"  # Mismatch!
        }
    ]
    is_valid, msg, broken_idx = verify_exported_receipt_chain(receipts)
    assert is_valid is False
    assert broken_idx == 1
    assert "[CORRUPTED]" in msg
