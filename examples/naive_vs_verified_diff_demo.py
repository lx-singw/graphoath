import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from graphoath.ops.diff_engine import NaiveVsVerifiedDiffEngine

def main():
    print("=======================================================================")
    print("GraphOath — Naive LLM vs. Citation-Gated Verified Claim Diff Showcase")
    print("=======================================================================")

    engine = NaiveVsVerifiedDiffEngine()
    
    source_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    naive_claim = (
        "Schema breaking change detected on urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD). "
        "Impacts verified downstream urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD) and "
        "hallucinated asset urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.hallucinated_table,PROD)."
    )
    naive_urns = [
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.hallucinated_table,PROD)"
    ]

    report = engine.run_diff(
        source_urn=source_urn,
        naive_claim_text=naive_claim,
        naive_urns=naive_urns
    )

    print(f"\n[SOURCE URN] : {report.source_urn}")
    print(f"[NAIVE CLAIM]: {report.naive_claim_text}")
    print(f"[NAIVE URNS ]: {report.naive_urns}")
    print("\n-----------------------------------------------------------------------")
    print(f"[VERIFIED CLAIM]       : {report.verified_claim_text}")
    print(f"[VERIFIED URNS]        : {report.verified_urns}")
    print(f"[DROPPED HALLUCINATIONS]: {report.dropped_hallucinations}")
    print(f"[BLAST RADIUS SAVED]   : {report.blast_radius_saved} downstream system write actions")
    print(f"[RESOLUTION RATE]      : {report.citation_resolution_rate * 100:.1f}%")
    print(f"[CUSTODY RECEIPT ID]   : {report.receipt_id}")
    print("=======================================================================\n")

if __name__ == "__main__":
    main()
