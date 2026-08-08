from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graphoath.config import settings
from graphoath.api import routes_auth, routes_receipts, routes_incidents, routes_calculator, routes_webhooks, routes_exports, routes_ledger, routes_approvals

app = FastAPI(
    title="GraphOath API",
    description="The Evidence Engine for Agentic Data Governance",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_auth.router, prefix="/api")
app.include_router(routes_receipts.router, prefix="/api")
app.include_router(routes_incidents.router, prefix="/api")
app.include_router(routes_calculator.router, prefix="/api")
app.include_router(routes_webhooks.router, prefix="/api/v1")
app.include_router(routes_webhooks.router, prefix="/api")
app.include_router(routes_exports.router, prefix="/api/v1")
app.include_router(routes_exports.router, prefix="/api")
app.include_router(routes_ledger.router, prefix="/api/v1")
app.include_router(routes_ledger.router, prefix="/api")
app.include_router(routes_approvals.router)


@app.get("/")
async def root():
    return {
        "service": "GraphOath API",
        "status": "online",
        "version": "0.1.0",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "environment": settings.environment}
