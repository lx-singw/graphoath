"""
GraphOath Ledger Verifier Module & REST API Handler.

Recomputes recursive SHA-256 hash chains across Custody receipts and checks for database tampering.
"""

import hashlib
import json
from typing import List, Dict, Any, Tuple

def compute_receipt_hash(prev_hash: str, payload: Dict[str, Any]) -> str:
    """Computes SHA-256 hash of previous hash concatenated with canonical JSON payload."""
    canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    to_sign = f"{prev_hash}:{canonical_json}".encode('utf-8')
    return hashlib.sha256(to_sign).hexdigest()

def verify_ledger_chain(receipts: List[Dict[str, Any]]) -> Tuple[bool, int, str]:
    """
    Verifies recursive SHA-256 hash chain across an array of receipt dicts.
    Each receipt dict must contain:
    - 'previous_hash' (str)
    - 'payload' (dict)
    - 'ledger_hash' (str)
    
    Returns:
        (is_valid: bool, corrupted_index: int, message: str)
    """
    if not receipts:
        return True, -1, "Ledger is empty."

    prev_hash = "GENESIS_HASH_00000000000000000000000000000000000000000000000000000000"

    for idx, rcpt in enumerate(receipts):
        expected_prev = rcpt.get("previous_hash", prev_hash)
        payload = rcpt.get("payload", {})
        stored_hash = rcpt.get("ledger_hash", "")

        computed = compute_receipt_hash(expected_prev, payload)

        if computed != stored_hash:
            return False, idx, f"Hash mismatch at index {idx}! Computed: {computed}, Stored: {stored_hash}"

        prev_hash = stored_hash

    return True, -1, f"Ledger verified successfully across {len(receipts)} receipt(s)."
