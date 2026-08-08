import pytest
from graphoath.modules.deposition.confidence import ConfidenceRoutingEngine, RoutingTier

def test_confidence_routing_direct_verified_owner():
    engine = ConfidenceRoutingEngine()
    res = engine.evaluate_confidence(
        hop_distance=1,
        owner_type="VERIFIED",
        last_queried_hours=2.0
    )
    assert res.confidence_score >= 0.90
    assert res.routing_tier == RoutingTier.AUTO_EXECUTE

def test_confidence_routing_fallback_owner_2hop():
    engine = ConfidenceRoutingEngine()
    res = engine.evaluate_confidence(
        hop_distance=2,
        owner_type="FALLBACK",
        last_queried_hours=12.0
    )
    # Hop=0.75 * 0.4 = 0.3, Owner=0.5 * 0.35 = 0.175, Usage=1.0 * 0.25 = 0.25 => Total = 0.725 -> 0.82 with 1-hop fallback
    assert 0.70 <= res.confidence_score < 0.90
    assert res.routing_tier == RoutingTier.HITL_APPROVAL_QUEUE

def test_confidence_routing_unassigned_3hop():
    engine = ConfidenceRoutingEngine()
    res = engine.evaluate_confidence(
        hop_distance=3,
        owner_type="UNASSIGNED",
        last_queried_hours=300.0  # >7d => 0.20
    )
    assert res.confidence_score < 0.75
    assert res.routing_tier == RoutingTier.REJECT
