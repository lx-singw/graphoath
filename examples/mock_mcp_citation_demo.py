#!/usr/bin/env python3
"""
GraphOath — Standalone End-to-End Citation Gate Demo Script

This script provides a standalone, zero-dependency demonstration of GraphOath's
citation-gated control plane mechanics:
1. Ingesting a DataHub Schema Change Event.
2. Querying a mock DataHub lineage graph (MCP / Agent Context Kit API).
3. Gate evaluation (pass vs reject).
4. Generating an immutable, hash-chained Custody receipt.

Usage:
    python examples/mock_mcp_citation_demo.py
"""

import hashlib
import json
import time

def compute_sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def run_citation_demo():
    print("----------------------------------------------------------------------")
    print("GraphOath Deposition Module — Mock DataHub MCP Citation Demo")
    print("----------------------------------------------------------------------")

    # Step 1: Simulate schema MetadataChangeLog event
    event = {
        "eventType": "MetadataChangeLog_v1",
        "entityType": "dataset",
        "entityUrn": "urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.public.users,PROD)",
        "changeType": "UPDATE",
        "aspectName": "schemaMetadata",
        "timestamp": int(time.time())
    }
    print(f"\n[Event Ingested] Inbound DataHub Event for: {event['entityUrn']}")

    # Step 2: Simulate Lineage & Metadata Context query via MCP Server
    evidence_graph = [
        {
            "urn": "urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.public.users,PROD)",
            "role": "source",
            "schema_fields": ["id", "email", "created_at"]
        },
        {
            "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_users,PROD)",
            "role": "downstream_hop_1",
            "owner": "urn:li:corpuser:alice_data_eng"
        },
        {
            "urn": "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.dim_customers,PROD)",
            "role": "downstream_hop_2",
            "owner": "urn:li:corpuser:analytics_team"
        }
    ]
    
    evidence_urns = {node["urn"] for node in evidence_graph}
    print(f"[Evidence Engine] Retrieved {len(evidence_graph)} nodes from DataHub lineage graph.")

    # Step 3: Citation Gate Evaluation
    valid_claim = (
        "Schema breaking change on urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.public.users,PROD) "
        "impacts downstream staging dataset urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_users,PROD) "
        "and dimension table urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.dim_customers,PROD)."
    )

    print("\n[Citation Gate] Evaluating proposed claim text...")
    print(f"Claim: '{valid_claim}'")

    # Verify URNs
    claimed_urns = [
        "urn:li:dataset:(urn:li:dataPlatform:postgres,analytics.public.users,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_users,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.dim_customers,PROD)"
    ]

    all_cited = all(urn in evidence_urns for urn in claimed_urns)

    if all_cited:
        print("\n[Gate Result] PASSED (100% Citation Resolution)")
        
        # Step 4: Custody Hash Chain Ledger Write
        prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
        receipt_body = {
            "receipt_id": "rcpt_mock_20260807_01",
            "module": "Deposition",
            "timestamp": event["timestamp"],
            "source_urn": event["entityUrn"],
            "claim": valid_claim,
            "evidence": list(evidence_urns),
            "action": "raiseIncident",
            "assigned_owner": "urn:li:corpuser:alice_data_eng",
            "prev_hash": prev_hash
        }

        receipt_json = json.dumps(receipt_body, sort_keys=True)
        current_hash = compute_sha256(receipt_json + prev_hash)

        print("\n[Custody Ledger] Written Receipt with SHA-256 Hash Chain:")
        print(f"Receipt ID   : {receipt_body['receipt_id']}")
        print(f"Action       : DataHub Native Incident raised (assignee: alice_data_eng)")
        print(f"Receipt Hash : {current_hash}")

    print("\n----------------------------------------------------------------------")
    print("Demo Script Completed Cleanly.")
    print("----------------------------------------------------------------------")

if __name__ == "__main__":
    run_citation_demo()
