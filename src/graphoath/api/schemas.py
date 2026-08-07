from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class UserInfo(BaseModel):
    id: str
    email: str
    role: str
    organization_id: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 43200
    user: UserInfo

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 43200

class ReceiptSummary(BaseModel):
    receipt_id: str
    module: str
    created_at: str
    trigger: Dict[str, Any]
    claim: str
    incident_urn: Optional[str] = None
    hash: str
    prev_hash: str

class ReceiptsListResponse(BaseModel):
    receipts: List[ReceiptSummary]
    next_cursor: Optional[str] = None
    total_count: int

class ReceiptDetailResponse(BaseModel):
    receipt_id: str
    module: str
    created_at: str
    trigger: Dict[str, Any]
    claim: str
    evidence: List[Dict[str, Any]]
    confidence: str
    action_taken: Dict[str, Any]
    hash: str
    prev_hash: str
    prior_receipts: List[str] = []
    memory_note: Optional[str] = None

class IncidentResponse(BaseModel):
    incident_urn: str
    status: str
    priority: str
    type: str
    assignees: List[str]
    created_at: str
    linked_receipts: List[str] = []

class ApprovalRequest(BaseModel):
    approver_note: Optional[str] = None

class DenialRequest(BaseModel):
    reason: str

class ApprovalResponse(BaseModel):
    action_id: str
    status: str
    approved_by: str
    approved_at: str
    receipt_id: Optional[str] = None

class LedgerVerifyResponse(BaseModel):
    status: str
    receipts_checked: int
    break_at_receipt_id: Optional[str] = None
    expected_hash: Optional[str] = None
    actual_hash: Optional[str] = None
    checked_at: str

class ExportRequest(BaseModel):
    from_date: str = "2026-01-01"
    to_date: str = "2026-12-31"
    format: str = "pdf"

class ExportResponse(BaseModel):
    export_id: str
    status: str
    requested_by: str
    estimated_completion_seconds: int = 12
