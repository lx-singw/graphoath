import pytest
from graphoath.modules.deposition.confidence import calculate_confidence_score

def test_confidence_score_tier_a():
    evidence = [
        {"type": "lineage", "hops": 1},
        {"type": "ownership", "result": "team-growth-analytics"},
        {"type": "usage", "result": "340 queries/week"}
    ]
    score, tier, requires_approval = calculate_confidence_score(evidence)
    assert score >= 0.90
    assert "Tier A" in tier
    assert requires_approval is False

def test_confidence_score_tier_b():
    evidence = [
        {"type": "lineage", "hops": 2},
        {"type": "ownership", "result": "team-growth-analytics"}
    ]
    score, tier, requires_approval = calculate_confidence_score(evidence)
    assert score < 0.90
    assert requires_approval is True
