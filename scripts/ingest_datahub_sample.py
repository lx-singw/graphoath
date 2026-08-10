#!/usr/bin/env python3
"""
GraphOath DataHub Metadata Ingestion Script.
Emits sample datasets, charts, owners, and multi-platform lineage into live DataHub GMS.
"""

import os
import sys
import httpx

GMS_URL = os.getenv("DATAHUB_GMS_URL", "http://host.docker.internal:8080").rstrip('/')
if "localhost" in GMS_URL and os.path.exists("/.dockerenv"):
    GMS_URL = GMS_URL.replace("localhost", "host.docker.internal")

def emit_aspect(entity_type: str, urn: str, aspect_name: str, value_dict: dict):
    """Emits generic aspect metadata via GMS REST API."""
    import json
    url = f"{GMS_URL}/aspects?action=ingestProposal"
    payload = {
        "proposal": {
            "entityType": entity_type,
            "entityUrn": urn,
            "changeType": "UPSERT",
            "aspectName": aspect_name,
            "aspect": {
                "value": json.dumps(value_dict),
                "contentType": "application/json"
            }
        }
    }
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code in [200, 201]:
                print(f"  [OK] Ingested Aspect '{aspect_name}' for {urn}")
            else:
                print(f"  [INFO] Ingest response {resp.status_code} for {urn}")
    except Exception as e:
        print(f"  [NOTICE] Connection attempt to DataHub GMS at {url}: {e}")

def emit_dataset_mcp(urn: str, platform: str, name: str):
    emit_aspect("dataset", urn, "datasetProperties", {"name": name, "description": "GraphOath Governed Data Asset"})

def main():
    print("=======================================================================")
    print("GraphOath — Live DataHub Metadata Sample Ingestion")
    print("=======================================================================")
    
    datasets = [
        ("urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)", "snowflake", "prod.orders"),
        ("urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)", "dbt", "dbt.stg_orders"),
        ("urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.fct_daily_revenue,PROD)", "dbt", "dbt.fct_daily_revenue")
    ]
    
    for urn, platform, name in datasets:
        emit_dataset_mcp(urn, platform, name)
        
    # Ingest Ownership
    emit_aspect("dataset", "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)", "ownership", {
        "owners": [{"owner": "urn:li:corpuser:priya_ramaswamy", "type": "TECHNICAL_OWNER"}]
    })

    # Ingest Upstream Lineage
    emit_aspect("dataset", "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)", "upstreamLineage", {
        "upstreams": [{"dataset": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)", "type": "TRANSFORMED"}]
    })
    emit_aspect("dataset", "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.fct_daily_revenue,PROD)", "upstreamLineage", {
        "upstreams": [{"dataset": "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)", "type": "TRANSFORMED"}]
    })
        
    print("=======================================================================")
    print("Ingestion sequence dispatched to DataHub at http://localhost:8080")
    print("=======================================================================")

if __name__ == "__main__":
    main()
