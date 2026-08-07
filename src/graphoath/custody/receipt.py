import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

@dataclass
class Receipt:
    receipt_id: str
    module: str
    created_at: str
    trigger_info: Dict[str, Any]
    claim: str
    evidence: List[Dict[str, Any]]
    action_taken: Dict[str, Any]
    prev_hash: str
    confidence: str = "high"
    prior_receipts: List[str] = field(default_factory=list)
    memory_note: Optional[str] = None
    hash: str = ""

    def __post_init__(self):
        if not self.hash:
            self.hash = self.compute_hash()

    def to_canonical_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "module": self.module,
            "created_at": self.created_at,
            "trigger": self.trigger_info,
            "claim": self.claim,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "action_taken": self.action_taken,
            "prior_receipts": self.prior_receipts,
            "memory_note": self.memory_note,
        }

    def compute_hash(self) -> str:
        canonical_json = json.dumps(
            self.to_canonical_dict(),
            sort_keys=True,
            separators=(',', ':')
        )
        payload = self.prev_hash + canonical_json
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
