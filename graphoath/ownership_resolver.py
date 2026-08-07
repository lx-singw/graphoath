"""
GraphOath Hierarchical Ownership & Domain Resolver Module.

Resolves assignees using DataHub's ownership hierarchy:
Dataset Owners -> Domain Leads -> Platform Admin Fallback.
"""

from typing import List, Dict, Any, Tuple

MOCK_OWNERSHIP_CATALOG = {
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)": {
        "owners": ["urn:li:corpuser:alice_data_owner"],
        "domain": "urn:li:domain:finance"
    },
    "urn:li:domain:finance": {
        "lead": "urn:li:corpuser:finance_domain_lead"
    }
}

DEFAULT_PLATFORM_ADMIN = "urn:li:corpuser:platform_admin_oncall"

def resolve_hierarchical_ownership(dataset_urn: str) -> Tuple[List[str], str]:
    """
    Resolves assignees hierarchically.
    Returns:
        (assignees: List[str], resolution_tier: str)
    """
    entry = MOCK_OWNERSHIP_CATALOG.get(dataset_urn)
    if entry:
        owners = entry.get("owners", [])
        if owners:
            return owners, "TIER_1_DIRECT_OWNER"
            
        domain_urn = entry.get("domain")
        if domain_urn and domain_urn in MOCK_OWNERSHIP_CATALOG:
            domain_lead = MOCK_OWNERSHIP_CATALOG[domain_urn].get("lead")
            if domain_lead:
                return [domain_lead], "TIER_2_DOMAIN_LEAD"
                
    return [DEFAULT_PLATFORM_ADMIN], "TIER_3_PLATFORM_ADMIN_FALLBACK"

if __name__ == "__main__":
    assignees, tier = resolve_hierarchical_ownership("urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")
    print(f"[GraphOath Ownership Resolver] Resolved {assignees} via {tier}")
    assert assignees == ["urn:li:corpuser:alice_data_owner"]
    assert tier == "TIER_1_DIRECT_OWNER"
