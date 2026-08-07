from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from graphoath.custody.receipt import Receipt, GENESIS_HASH
from graphoath.custody.models import ReceiptModel

class Ledger:
    def __init__(self, db_session: Optional[Session] = None):
        self.db = db_session
        self._memory_ledger: List[Receipt] = []

    def get_latest_hash(self) -> str:
        if self.db:
            latest = self.db.query(ReceiptModel).order_by(ReceiptModel.created_at.desc()).first()
            if latest:
                return str(latest.hash)
            return GENESIS_HASH
        else:
            if self._memory_ledger:
                return self._memory_ledger[-1].hash
            return GENESIS_HASH

    def append_receipt(self, receipt: Receipt) -> Receipt:
        latest_hash = self.get_latest_hash()
        receipt.prev_hash = latest_hash
        receipt.hash = receipt.compute_hash()

        if self.db:
            db_receipt = ReceiptModel(
                receipt_id=receipt.receipt_id,
                module=receipt.module,
                created_at=receipt.created_at,
                trigger_info=receipt.trigger_info,
                claim=receipt.claim,
                evidence=receipt.evidence,
                confidence=receipt.confidence,
                action_taken=receipt.action_taken,
                hash=receipt.hash,
                prev_hash=receipt.prev_hash,
                prior_receipts=receipt.prior_receipts,
                memory_note=receipt.memory_note
            )
            self.db.add(db_receipt)
            self.db.commit()
            self.db.refresh(db_receipt)
        else:
            self._memory_ledger.append(receipt)

        return receipt

    def verify_chain(self) -> Tuple[bool, int, Optional[str]]:
        """
        Verifies SHA-256 hash-chain integrity.
        Returns: (is_intact, receipts_checked, break_at_receipt_id)
        """
        if self.db:
            db_receipts = self.db.query(ReceiptModel).order_by(ReceiptModel.created_at.asc()).all()
            receipts = [
                Receipt(
                    receipt_id=r.receipt_id,
                    module=r.module,
                    created_at=r.created_at.isoformat() if hasattr(r.created_at, 'isoformat') else str(r.created_at),
                    trigger_info=r.trigger_info,
                    claim=r.claim,
                    evidence=r.evidence,
                    confidence=r.confidence,
                    action_taken=r.action_taken,
                    prev_hash=r.prev_hash,
                    prior_receipts=r.prior_receipts or [],
                    memory_note=r.memory_note,
                    hash=r.hash
                )
                for r in db_receipts
            ]
        else:
            receipts = self._memory_ledger

        expected_prev_hash = GENESIS_HASH
        for idx, r in enumerate(receipts):
            if r.prev_hash != expected_prev_hash:
                return False, idx, r.receipt_id
            if r.compute_hash() != r.hash:
                return False, idx, r.receipt_id
            expected_prev_hash = r.hash

        return True, len(receipts), None
