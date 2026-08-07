from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from graphoath.db.session import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="operator")
    organization_id = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

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
