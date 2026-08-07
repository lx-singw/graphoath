#!/usr/bin/env python3
"""
GraphOath — LangChain / LangGraph Agent Integration Example

This runnable example demonstrates how an AI agent built with LangChain / LangGraph:
1. Queries metadata context from DataHub (via MCP / Agent Context Kit).
2. Assembles a draft incident claim based on a detected schema break.
3. Passes the claim through GraphOath's Citation Gate (`verify_claim`).
4. Executes a native DataHub Incident creation action with a tamper-evident receipt.

Usage:
    python examples/langchain_agent_example.py
"""

import json
import dataclasses
from typing import List, Dict, Any, Tuple

# --- Step 1: Mock DataHub MCP / Context Kit Response ---

MOCK_DATAHUB_LINEAGE = [
    {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "name": "prod.orders",
        "type": "upstream_source",
    },
    {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)",
        "name": "prod.stg_orders",
        "type": "downstream_staging",
        "owner": "urn:li:corpuser:data_eng_team",
    },
    {
        "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fct_daily_revenue,PROD)",
        "name": "prod.fct_daily_revenue",
        "type": "downstream_fact",
        "owner": "urn:li:corpuser:finance_analytics",
    },
]

import re

# --- Step 2: GraphOath Citation Gate Core Logic ---

@dataclasses.dataclass
class CitationGateResult:
    passed: bool
    evidence_count: int
    missing_citations: List[str]
    receipt_hash: str

class GraphOathCitationGate:
    """Zero-network citation verification engine."""

    def verify_claim(self, claim_text: str, evidence_urns: List[str]) -> CitationGateResult:
        # Extract URN references cleanly using regex
        pattern = r"urn:li:[a-zA-Z0-9_]+:\([^)]+\)"
        referenced_urns = re.findall(pattern, claim_text)
        if not referenced_urns:
            # Fallback for simple URN format without parens
            pattern_fallback = r"urn:li:[a-zA-Z0-9_]+:[a-zA-Z0-9_\-]+"
            referenced_urns = re.findall(pattern_fallback, claim_text)

        unmatched = [urn for urn in referenced_urns if urn not in evidence_urns]

        # Generate mock SHA-256 hash for tamper-evident ledger
        receipt_hash = f"sha256_{hash(claim_text + ''.join(evidence_urns)) & 0xffffffff:08x}"

        if unmatched:
            return CitationGateResult(
                passed=False,
                evidence_count=len(evidence_urns),
                missing_citations=unmatched,
                receipt_hash=receipt_hash
            )
        
        return CitationGateResult(
            passed=True,
            evidence_count=len(evidence_urns),
            missing_citations=[],
            receipt_hash=receipt_hash
        )

# --- Step 3: Simulated LangChain Tool Execution ---

def run_langchain_agent_workflow():
    print("=" * 70)
    print("GraphOath + LangChain Agent Integration Example")
    print("=" * 70)

    # 1. Fetch evidence URNs from DataHub Context Kit
    evidence_urns = [item["urn"] for item in MOCK_DATAHUB_LINEAGE]
    source_urn = MOCK_DATAHUB_LINEAGE[0]["urn"]

    print(f"\n[1] Fetched DataHub Evidence Context (3 assets in lineage graph):")
    for urn in evidence_urns:
        print(f"    - {urn}")

    gate = GraphOathCitationGate()

    # 2. Scenario A: Agent attempts an UNVALIDATED / HALLUCINATED claim
    bad_claim = (
        f"Schema change on {source_urn} breaks downstream asset "
        f"urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.hallucinated_table,PROD)!"
    )
    print(f"\n[2] Agent proposing Draft Claim (Scenario A - Uncited URN):")
    print(f"    '{bad_claim}'")

    result_a = gate.verify_claim(bad_claim, evidence_urns)
    print(f"\n[3] GraphOath Citation Gate Evaluation:")
    if not result_a.passed:
        print(f"    [X] REJECTED! Uncited entities named: {result_a.missing_citations}")
        print("    -> Action blocked from hitting DataHub API.")

    # 3. Scenario B: Agent produces a VALID CITED claim
    good_claim = (
        f"Schema change on {source_urn} breaks downstream staging table "
        f"urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD) and fact table "
        f"urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fct_daily_revenue,PROD)."
    )
    print(f"\n[4] Agent proposing Revised Draft Claim (Scenario B - Valid Citations):")
    print(f"    '{good_claim}'")

    result_b = gate.verify_claim(good_claim, evidence_urns)
    print(f"\n[5] GraphOath Citation Gate Evaluation:")
    if result_b.passed:
        print(f"    [OK] PASSED! All named entities verified against DataHub evidence array.")
        print(f"    -> Emitting Native DataHub Incident (raiseIncident)")
        print(f"    -> Writing Receipt Hash to Custody Ledger: {result_b.receipt_hash}")
        
        receipt_payload = {
            "receipt_id": "rcpt_langchain_demo_001",
            "source_urn": source_urn,
            "claim": good_claim,
            "evidence_urn_count": result_b.evidence_count,
            "ledger_hash": result_b.receipt_hash,
            "datahub_mutation": "raiseIncident"
        }
        print("\n[6] Generated Custody Receipt Aspect:")
        print(json.dumps(receipt_payload, indent=2))

    print("\n" + "=" * 70)
    print("Demo Execution Completed Successfully!")
    print("=" * 70)

if __name__ == "__main__":
    run_langchain_agent_workflow()
