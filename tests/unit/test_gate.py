import pytest
from graphoath.modules.deposition.gate import validate_citation_gate

def test_validate_citation_gate_approved():
    claim = "Removing customer_region will affect churn-overview and churn_model_v3"
    evidence = [
        {"type": "lineage", "result_urn": "urn:li:dashboard:(looker,churn-overview)"},
        {"type": "lineage", "result_urn": "urn:li:mlFeatureTable:(churn_model_v3,region_bucket)"}
    ]
    is_approved, finalized, unsupported = validate_citation_gate(claim, evidence)
    assert is_approved is True
    assert unsupported == []

def test_validate_citation_gate_rejected():
    claim = "Removing customer_region will affect churn-overview and unknown_dashboard_xyz"
    evidence = [
        {"type": "lineage", "result_urn": "urn:li:dashboard:(looker,churn-overview)"}
    ]
    # If claim mentions churn_model_v3 but not in evidence
    claim_with_unsupported = "Removing customer_region will affect churn-overview and churn_model_v3"
    is_approved, finalized, unsupported = validate_citation_gate(claim_with_unsupported, evidence)
    assert is_approved is False
    assert "churn_model_v3" in unsupported
