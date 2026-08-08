from typing import Any

try:
    from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, BigInteger, Float
    from sqlalchemy.sql import func
    from graphoath.db.session import Base
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    class _Dummy:
        def __init__(self, *args, **kwargs): pass
        def __call__(self, *args, **kwargs): return self
        def __getattr__(self, name): return self
    Column = String = Text = DateTime = JSON = ForeignKey = BigInteger = Float = func = _Dummy()  # type: ignore
    class Base:  # type: ignore
        metadata = None

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="operator")
    organization_id = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CustodyReceiptModel(Base):
    __tablename__ = "custody_receipts"

    id = Column(BigInteger if hasattr(Base, 'BigInteger') else String(64), primary_key=True, autoincrement=True)
    receipt_id = Column(String(64), unique=True, nullable=False)
    sequence_number = Column(BigInteger if hasattr(Base, 'BigInteger') else Column(String(64)), unique=True, nullable=False)
    previous_hash = Column(String(64), nullable=False)
    current_hash = Column(String(64), nullable=False)
    agent_id = Column(String(255), nullable=False)
    spiffe_id = Column(String(255), nullable=False, default="spiffe://graphoath.io/agent/deposition-v1")
    svid_serial = Column(String(128), default="svid-serial-0001")
    action_type = Column(String(128), nullable=False)
    target_urn = Column(String(512), nullable=False)
    evidence_payload = Column(JSON, nullable=False)
    claims_payload = Column(JSON, nullable=False)
    gate_decision = Column(String(32), nullable=False, default="APPROVED")
    confidence_score = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LedgerAuditLogModel(Base):
    __tablename__ = "ledger_audit_log"

    id = Column(BigInteger if hasattr(Base, 'BigInteger') else String(64), primary_key=True, autoincrement=True)
    verification_id = Column(String(64), unique=True, nullable=False)
    status = Column(String(32), nullable=False)
    total_records_checked = Column(BigInteger if hasattr(Base, 'BigInteger') else Column(String(64)), nullable=False)
    tampered_receipt_id = Column(String(64), nullable=True)
    execution_time_ms = Column(Float, nullable=False)
    verified_at = Column(DateTime(timezone=True), server_default=func.now())

class HITLApprovalModel(Base):
    __tablename__ = "hitl_approvals"

    id = Column(BigInteger if hasattr(Base, 'BigInteger') else String(64), primary_key=True, autoincrement=True)
    approval_id = Column(String(64), unique=True, nullable=False)
    receipt_id = Column(String(64), ForeignKey("custody_receipts.receipt_id"), nullable=True)
    status = Column(String(32), nullable=False, default="PENDING")
    requested_by_spiffe_id = Column(String(255), nullable=False)
    approved_by_user = Column(String(255), nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

class ReceiptModel(Base):
    __tablename__ = "receipts"

    receipt_id = Column(String(128), primary_key=True)
    module = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    trigger_info = Column(JSON, nullable=False)
    claim = Column(Text, nullable=False)
    evidence = Column(JSON, nullable=False)
    confidence = Column(String(20), nullable=False, default="high")
    action_taken = Column(JSON, nullable=False)
    hash = Column(String(64), nullable=False)
    prev_hash = Column(String(64), nullable=False)
    prior_receipts = Column(JSON, default=list)
    memory_note = Column(Text, nullable=True)

class ApprovalActionModel(Base):
    __tablename__ = "approval_actions"

    action_id = Column(String(64), primary_key=True)
    receipt_id = Column(String(128), ForeignKey("receipts.receipt_id"), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    requires_role = Column(String(50), nullable=False, default="operator")
    approver_note = Column(Text, nullable=True)
    approved_by = Column(String(64), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

