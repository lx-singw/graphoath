"""
GraphOath OpenAPI Specification Exporter.

Exports machine-readable OpenAPI v3.1 JSON/YAML specs for API contract testing.
"""

import json
import os

def generate_mock_openapi_spec() -> dict:
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "GraphOath Agent Safety Harness & Control Plane REST API",
            "version": "1.0.0",
            "description": "OpenAPI specification for GraphOath citation gating, Custody ledger, and incident triage."
        },
        "paths": {
            "/api/v1/ledger/verify": {
                "get": {
                    "summary": "Verify Custody Ledger SHA-256 Hash Chain Integrity",
                    "responses": {
                        "200": {
                            "description": "Ledger intact",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "status": "HEALTHY",
                                        "is_valid": True,
                                        "verified_receipt_count": 1403
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/gate/evaluate": {
                "post": {
                    "summary": "Evaluate Agent Claim against DataHub Metadata Evidence",
                    "responses": {
                        "200": {
                            "description": "Gate evaluation result",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "status": "APPROVED",
                                        "citation_resolution_rate": 1.0
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

def main():
    os.makedirs("docs", exist_ok=True)
    spec = generate_mock_openapi_spec()
    out_json = os.path.join("docs", "openapi.json")
    with open(out_json, "w") as f:
        json.dump(spec, f, indent=2)
    print(f"[OpenAPI Exporter] Exported OpenAPI specification to {out_json}")

if __name__ == "__main__":
    main()
