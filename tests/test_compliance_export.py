import pytest
from fastapi.testclient import TestClient
from graphoath.main import app

client = TestClient(app)

def test_get_compliance_export_json_schema():
    response = client.get("/api/v1/compliance/export?format=json")
    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    
    data = response.json()
    assert "compliance_standard" in data
    assert "EU AI Act Article 12 & 14" in data["compliance_standard"]
    assert "verification_status" in data
    assert "receipts" in data
