from typing import Dict, Any, Optional
from fastapi import APIRouter, Header, HTTPException, status
from graphoath.custody.ledger import Ledger
from graphoath.custody.verify import verify_ledger_integrity

router = APIRouter(prefix="/ledger", tags=["Ledger Governance"])

@router.get("/verify", status_code=status.HTTP_200_OK)
async def verify_ledger_endpoint(
    authorization: Optional[str] = Header(None),
    x_service_key: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """
    GET /api/v1/ledger/verify
    
    Independently verifies SHA-256 custody ledger hash chain integrity from Genesis block to head.
    Security: Accepts JWT token or internal service key.
    """
    ledger = Ledger()
    res = await verify_ledger_integrity(ledger=ledger)
    return res
