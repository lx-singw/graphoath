from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from graphoath.config import settings
from graphoath.telemetry import metrics_registry
from graphoath.api import (
    routes_auth,
    routes_receipts,
    routes_incidents,
    routes_calculator,
    routes_webhooks,
    routes_exports,
    routes_ledger,
    routes_approvals,
    routes_gate
)

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

# Active WebSocket connections manager
class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

ws_manager = WebSocketConnectionManager()

app.include_router(routes_auth.router, prefix="/api/v1")
app.include_router(routes_receipts.router, prefix="/api/v1")
app.include_router(routes_incidents.router, prefix="/api/v1")
app.include_router(routes_calculator.router, prefix="/api/v1")
app.include_router(routes_webhooks.router, prefix="/api/v1")
app.include_router(routes_exports.router, prefix="/api/v1")
app.include_router(routes_ledger.router, prefix="/api/v1")
app.include_router(routes_approvals.router)
app.include_router(routes_gate.router, prefix="/api/v1")

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

@app.get("/metrics", response_class=PlainTextResponse)
async def get_metrics():
    """Exposes Prometheus metrics endpoint."""
    return metrics_registry.generate_prometheus_text()

@app.websocket("/api/v1/ws/stream")
async def websocket_event_stream(websocket: WebSocket):
    """Real-time WebSocket event stream for incidents, evaluations, and receipts."""
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back keepalive / ping
            await websocket.send_json({"event": "ack", "data": data})
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
