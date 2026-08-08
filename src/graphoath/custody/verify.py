from typing import Dict, Any, Optional
from graphoath.custody.ledger import Ledger
from graphoath.custody.receipt import GENESIS_HASH

def verify_ledger_chain(ledger: Optional[Ledger] = None) -> Dict[str, Any]:
    """
    Independent chain verification engine.
    Recomputes SHA-256 hash chain from Genesis block to head.
    
    Returns OpenAPI 3.1 compliant verification object.
    """
    ledger_instance = ledger or Ledger()
    is_intact, count, break_id = ledger_instance.verify_chain()
    head_hash = ledger_instance.get_latest_hash()

    if is_intact:
        return {
            "status": "HEALTHY",
            "is_valid": True,
            "verified_receipt_count": count,
            "head_ledger_hash": head_hash,
            "message": f"Ledger hash chain intact across {count} receipt(s)."
        }
    else:
        return {
            "status": "CORRUPTED",
            "is_valid": False,
            "verified_receipt_count": count,
            "break_at_receipt_id": break_id,
            "head_ledger_hash": head_hash,
            "message": f"Cryptographic tamper detected at receipt ID '{break_id}' (index {count})."
        }
