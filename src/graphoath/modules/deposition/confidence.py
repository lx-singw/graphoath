from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from graphoath.datahub.lineage import EvidencePackage

class RoutingTier(str, Enum):
    AUTO_EXECUTE = "AUTO_EXECUTE"
    HITL_APPROVAL_QUEUE = "HITL_APPROVAL_QUEUE"
    REJECT = "REJECT"

class ConfidenceResult(BaseModel):
    confidence_score: float
    routing_tier: RoutingTier
    hop_proximity_score: float
    ownership_score: float
    usage_recency_score: float
    explanation: str

class ConfidenceRoutingEngine:
    """
    Calculates Evidence Confidence Score for proposed agent actions:
    Confidence Score = w1 * HopProximity + w2 * OwnershipResolution + w3 * UsageRecency
    Weights: w1 = 0.40, w2 = 0.35, w3 = 0.25
    """
    def __init__(
        self,
        w1: float = 0.40,
        w2: float = 0.35,
        w3: float = 0.25
    ):
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3

    def evaluate_confidence(
        self,
        evidence_package: Optional[EvidencePackage] = None,
        hop_distance: int = 1,
        owner_type: str = "VERIFIED",  # VERIFIED, FALLBACK, UNASSIGNED
        last_queried_hours: float = 1.0
    ) -> ConfidenceResult:
        # If evidence package passed, extract metrics dynamically
        if evidence_package:
            hop_distance = evidence_package.max_hop_distance
            owner_type = evidence_package.ownership_status
            last_queried_hours = evidence_package.last_queried_hours

        # 1. Hop Proximity
        if hop_distance <= 1:
            hop_score = 1.0
        elif hop_distance == 2:
            hop_score = 0.75
        else:
            hop_score = 0.40

        # 2. Ownership Resolution
        owner_upper = str(owner_type).upper()
        if owner_upper in ("VERIFIED", "VERIFIED_OWNER", "TIER_1_DIRECT_OWNER"):
            owner_score = 1.0
        elif owner_upper in ("FALLBACK", "FALLBACK_TEAM", "TEAM"):
            owner_score = 0.75
        else:
            owner_score = 0.0

        # 3. Usage Recency
        if last_queried_hours <= 24:
            usage_score = 1.0
        elif last_queried_hours <= 168: # 7 days
            usage_score = 0.70
        else:
            usage_score = 0.20

        # Weighted calculation
        total_score = round(
            self.w1 * hop_score + self.w2 * owner_score + self.w3 * usage_score, 4
        )

        if total_score >= 0.90:
            tier = RoutingTier.AUTO_EXECUTE
        elif total_score >= 0.75:
            tier = RoutingTier.HITL_APPROVAL_QUEUE
        else:
            tier = RoutingTier.REJECT

        explanation = (
            f"Confidence score {total_score:.4f} (Hop={hop_score}, Owner={owner_score}, Usage={usage_score}) "
            f"routed to {tier.value}."
        )

        return ConfidenceResult(
            confidence_score=total_score,
            routing_tier=tier,
            hop_proximity_score=hop_score,
            ownership_score=owner_score,
            usage_recency_score=usage_score,
            explanation=explanation
        )
