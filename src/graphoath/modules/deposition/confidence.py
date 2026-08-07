from typing import List, Dict, Any, Tuple

def calculate_confidence_score(evidence: List[Dict[str, Any]]) -> Tuple[float, str, bool]:
    """
    Evaluates Evidence Confidence Score based on lineage hop distance,
    ownership resolution, and usage statistics.
    Returns: (confidence_score, tier_label, requires_human_approval)
    """
    if not evidence:
        return 0.50, "Tier C (Low)", True

    lineage_hops = [item.get("hops", 1) for item in evidence if item.get("type") == "lineage"]
    min_hops = min(lineage_hops) if lineage_hops else 3
    has_owner = any(item.get("type") == "ownership" for item in evidence)
    has_usage = any(item.get("type") == "usage" for item in evidence)

    score = 1.0
    if min_hops == 1:
        score *= 0.95
    elif min_hops == 2:
        score *= 0.85
    else:
        score *= 0.70

    if has_owner:
        score *= 1.0
    else:
        score *= 0.85

    if has_usage:
        score *= 1.0

    score = round(score, 2)

    if score >= 0.90:
        return score, "Tier A (High)", False
    elif score >= 0.75:
        return score, "Tier B (Medium)", True
    else:
        return score, "Tier C (Low)", True
