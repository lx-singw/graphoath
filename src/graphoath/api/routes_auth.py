from fastapi import APIRouter, HTTPException, status
from graphoath.api.schemas import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse, UserInfo

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest):
    if not body.email or not body.password:
        raise HTTPException(status_code=422, detail="Email and password required")
    
    # Mock user auth validation
    user = UserInfo(
        id="usr_3f7a9c",
        email=body.email,
        role="operator",
        organization_id="org_8b2e1f"
    )
    return LoginResponse(
        access_token="mock_access_token_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        refresh_token="rtok_8f3e9c2a1b4d6e7f9a0c1b2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f",
        user=user
    )

@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(body: RefreshRequest):
    if not body.refresh_token:
        raise HTTPException(status_code=422, detail="Refresh token required")
    return RefreshResponse(
        access_token="mock_refreshed_access_token_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    )
