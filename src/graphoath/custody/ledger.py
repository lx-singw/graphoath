import uuid
import time
from typing import List, Optional, Tuple, Dict, Any

try:
    from sqlalchemy.orm import Session
    from graphoath.custody.models import ReceiptModel, CustodyReceiptModel
    HAS_SQLALCHEMY = True
except ImportError:
    Session = Any  # type: ignore
    ReceiptModel = Any  # type: ignore
    CustodyReceiptModel = Any  # type: ignore
    HAS_SQLALCHEMY = False

from graphoath.custody.receipt import Receipt, CustodyReceipt, GENESIS_HASH

class Ledger:
    _memory_ledger: List[Receipt] = []
    _memory_custody_ledger: List[CustodyReceipt] = []

    @classmethod
    def clear_memory(cls):
        cls._memory_ledger.clear()
        cls._memory_custody_ledger.clear()

    def __init__(self, db_session: Optional[Session] = None):
        self.db = db_session

    def get_latest_hash(self) -> str:
        if self.db:
            try:
                latest = self.db.query(CustodyReceiptModel).order_by(CustodyReceiptModel.sequence_number.desc()).first()
                if latest:
                    return str(latest.current_hash)
            except Exception:
                pass
            try:
                latest_old = self.db.query(ReceiptModel).order_by(ReceiptModel.created_at.desc()).first()
                if latest_old:
                    return str(latest_old.hash)
            except Exception:
                pass
            return GENESIS_HASH
        else:
            if self._memory_custody_ledger:
                return self._memory_custody_ledger[-1].current_hash
            if self._memory_ledger:
                return self._memory_ledger[-1].hash
            return GENESIS_HASH

    def append_custody_receipt(self, receipt: CustodyReceipt) -> CustodyReceipt:
        latest_hash = self.get_latest_hash()
        receipt.previous_hash = latest_hash
        receipt.sequence_number = len(self._memory_custody_ledger) + 1
        receipt.current_hash = receipt.compute_hash()

        if self.db:
            try:
                db_model = CustodyReceiptModel(
                    receipt_id=receipt.receipt_id,
                    sequence_number=receipt.sequence_number,
                    previous_hash=receipt.previous_hash,
                    current_hash=receipt.current_hash,
                    agent_id=receipt.agent_id,
                    spiffe_id=receipt.spiffe_id,
                    svid_serial=receipt.svid_serial,
                    action_type=receipt.action_type,
                    target_urn=receipt.target_urn,
                    evidence_payload=receipt.evidence_payload,
                    claims_payload=receipt.claims_payload,
                    gate_decision=receipt.gate_decision,
                    confidence_score=receipt.confidence_score
                )
                self.db.add(db_model)
                self.db.commit()
                self.db.refresh(db_model)
            except Exception as e:
                print(f"[Ledger DB Warning] Persistence fallback: {e}")
                self._memory_custody_ledger.append(receipt)
        else:
            self._memory_custody_ledger.append(receipt)

        return receipt

    def append_receipt(self, receipt: Receipt) -> Receipt:
        latest_hash = self.get_latest_hash()
        receipt.prev_hash = latest_hash
        receipt.hash = receipt.compute_hash()

        if self.db:
            try:
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
            except Exception:
                self._memory_ledger.append(receipt)
        else:
            self._memory_ledger.append(receipt)

        return receipt

    def get_all_receipts(self) -> List[Any]:
        if self._memory_custody_ledger:
            return self._memory_custody_ledger
        return self._memory_ledger

    def verify_chain(self) -> Tuple[bool, int, Optional[str]]:
        """
        Verifies SHA-256 hash-chain integrity.
        Returns: (is_intact, receipts_checked, break_at_receipt_id)
        """
        if self._memory_custody_ledger:
            expected_prev_hash = GENESIS_HASH
            for idx, r in enumerate(self._memory_custody_ledger):
                if r.previous_hash != expected_prev_hash:
                    return False, idx, r.receipt_id
                if r.compute_hash() != r.current_hash:
                    return False, idx, r.receipt_id
                expected_prev_hash = r.current_hash
            return True, len(self._memory_custody_ledger), None

        if self.db:
            try:
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
            except Exception:
                receipts = self._memory_ledger
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

class LedgerEngine(Ledger):
    """Async & Sync High-Performance Custody Ledger Engine."""
    
    async def append_receipt(self, receipt: CustodyReceipt) -> CustodyReceipt:
        return self.append_custody_receipt(receipt)

    async def get_latest_hash_async(self) -> str:
        return self.get_latest_hash()


