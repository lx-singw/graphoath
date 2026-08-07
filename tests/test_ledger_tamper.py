"""
Pytest Test Suite for GraphOath Custody Ledger Tamper Detection.
"""

import unittest
from graphoath.ledger_verify import compute_receipt_hash, verify_ledger_chain

class TestLedgerTamperDetection(unittest.TestCase):
    def setUp(self):
        self.genesis_prev = "GENESIS_HASH_00000000000000000000000000000000000000000000000000000000"
        
        # Build 3 valid receipts in sequence
        p1 = {"receipt_id": "rcpt_1", "claim": "Valid claim 1", "source_urn": "urn:li:dataset:1"}
        h1 = compute_receipt_hash(self.genesis_prev, p1)
        r1 = {"previous_hash": self.genesis_prev, "payload": p1, "ledger_hash": h1}
        
        p2 = {"receipt_id": "rcpt_2", "claim": "Valid claim 2", "source_urn": "urn:li:dataset:2"}
        h2 = compute_receipt_hash(h1, p2)
        r2 = {"previous_hash": h1, "payload": p2, "ledger_hash": h2}
        
        p3 = {"receipt_id": "rcpt_3", "claim": "Valid claim 3", "source_urn": "urn:li:dataset:3"}
        h3 = compute_receipt_hash(h2, p3)
        r3 = {"previous_hash": h2, "payload": p3, "ledger_hash": h3}
        
        self.clean_ledger = [r1, r2, r3]

    def test_clean_ledger_passes(self):
        is_valid, idx, msg = verify_ledger_chain(self.clean_ledger)
        self.assertTrue(is_valid)
        self.assertEqual(idx, -1)

    def test_tampered_payload_fails(self):
        import copy
        tampered_ledger = copy.deepcopy(self.clean_ledger)
        # Modify payload in 2nd receipt without updating hash
        tampered_ledger[1]["payload"]["claim"] = "TAMPERED CLAIM VALUE!"
        
        is_valid, idx, msg = verify_ledger_chain(tampered_ledger)
        self.assertFalse(is_valid)
        self.assertEqual(idx, 1)
        self.assertIn("Hash mismatch at index 1", msg)

    def test_tampered_hash_fails(self):
        import copy
        tampered_ledger = copy.deepcopy(self.clean_ledger)
        # Modify hash string directly
        tampered_ledger[0]["ledger_hash"] = "0000000000000000000000000000000000000000000000000000000000000000"
        
        is_valid, idx, msg = verify_ledger_chain(tampered_ledger)
        self.assertFalse(is_valid)
        self.assertEqual(idx, 0)

if __name__ == "__main__":
    unittest.main()
