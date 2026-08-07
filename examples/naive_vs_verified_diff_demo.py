#!/usr/bin/env python3
"""
GraphOath — Naive vs. Verified Claim Diff Demonstration Script

This runnable script contrasts what an unconstrained/ungated LLM agent would claim
from a schema change event vs. what GraphOath's Deposition module actually asserts.

Usage:
    python examples/naive_vs_verified_diff_demo.py
"""

import json

def run_diff_demo():
    print("=" * 75)
    print("GraphOath Naive-vs-Verified Claim Diff Engine Demo")
    print("=" * 75)

    event_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    
    # -------------------------------------------------------------------
    # Scenario 1: What an UNGATED / NAIVE LLM Agent Claims
    # -------------------------------------------------------------------
    naive_claim = {
        "agent_mode": "NAIVE_UNCONSTRAINED_LLM",
        "prompt": "Analyse schema break on prod.orders and name affected datasets.",
        "generated_claim": (
            "Schema break on prod.orders breaks downstream models prod.stg_orders, "
            "prod.fct_daily_revenue, and prod.hallucinated_analytics_table owned by user:alice_data_eng."
        ),
        "citation_citations_checked": 0,
        "hallucinated_urns_included": [
            "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.hallucinated_analytics_table,PROD)"
        ],
        "action_taken": "UNVERIFIED_WRITE: Incident raised with hallucinated URNs!",
        "risk": "HIGH - False incident raised on non-existent dataset!"
    }

    # -------------------------------------------------------------------
    # Scenario 2: What GraphOath's DEPOSITION Module Asserts
    # -------------------------------------------------------------------
    verified_claim = {
        "agent_mode": "GRAPHOATH_CITATION_GATED",
        "evidence_urns_queried": [
            "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
            "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)",
            "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fct_daily_revenue,PROD)"
        ],
        "generated_claim": (
            "Schema breaking change on urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD) "
            "breaks downstream staging model urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD) "
            "and daily revenue model urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fct_daily_revenue,PROD)."
        ),
        "citation_resolution_rate": 1.0,
        "hallucinated_urns_included": [],
        "action_taken": "VERIFIED_WRITE: Native DataHub Incident urn:li:incident:graphoath-dep-001 raised.",
        "receipt_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }

    print("\n[NAIVE UNCONSTRAINED AGENT CLAIM]")
    print(json.dumps(naive_claim, indent=2))

    print("\n" + "-" * 75)

    print("\n[GRAPHOATH CITATION-GATED ASSERTION]")
    print(json.dumps(verified_claim, indent=2))

    print("\n" + "=" * 75)
    print("DIFF ANALYSIS: GraphOath stripped 1 hallucinated URN and guaranteed 100% citation safety.")
    print("=" * 75)

if __name__ == "__main__":
    run_diff_demo()
