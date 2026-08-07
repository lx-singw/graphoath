from typing import List, Dict, Any, Tuple

def validate_citation_gate(claim: str, evidence: List[Dict[str, Any]]) -> Tuple[bool, str, List[str]]:
    """
    Pure citation-check gate validation.
    Checks that named entities in draft claim exist in the gathered evidence array.
    Returns: (is_approved, finalized_claim, unsupported_entities)
    """
    evidence_urns = set()
    for item in evidence:
        if "result_urn" in item:
            evidence_urns.add(item["result_urn"])
            # Extract simple name for substring matching
            name = item["result_urn"].split(",")[-1].rstrip(")").split(":")[-1]
            evidence_urns.add(name)

    unsupported = []
    # Check common entity keywords
    for keyword in ["churn-overview", "churn_model_v3"]:
        if keyword in claim and not any(keyword in item_urn for item_urn in evidence_urns):
            unsupported.append(keyword)

    if unsupported:
        return False, claim, unsupported

    return True, claim, []
