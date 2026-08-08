import pytest
from graphoath.ops.diff_engine import NaiveVsVerifiedDiffEngine

def test_diff_engine_identifies_hallucinations():
    engine = NaiveVsVerifiedDiffEngine()
    source_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    naive_claim = "Deprecate prod.orders and prod.hallucinated_table"
    naive_urns = [
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.hallucinated_table,PROD)"
    ]

    report = engine.run_diff(source_urn=source_urn, naive_claim_text=naive_claim, naive_urns=naive_urns)

    assert report.source_urn == source_urn
    assert len(report.dropped_hallucinations) == 1
    assert "prod.hallucinated_table" in report.dropped_hallucinations[0]
    assert len(report.verified_urns) == 1
    assert report.blast_radius_saved == 3
    assert report.receipt_id.startswith("rcpt_diff_")
