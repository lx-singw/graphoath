import pytest
from fastapi.testclient import TestClient
from graphoath.main import app

client = TestClient(app)

def test_request_compliance_export():
    payload = {"format": "csv"}
    response = client.post("/api/v1/exports", json=payload)
    assert response.status_code == 202
    data = response.json()
    assert "export_id" in data
    assert data["status"] == "COMPLETED"

def test_download_compliance_export_csv():
    response = client.get("/api/v1/exports/exp_12345?format=csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "ReceiptID" in response.text
