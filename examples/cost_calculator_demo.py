"""
GraphOath Financial Cost of Hallucination ROI Calculator Demo.

Calculates quantifiable financial risk saved by enforcing zero-trust citation gating.
"""

def calculate_hallucination_cost_savings(
    annual_agent_actions: int = 5000,
    hallucination_rate: float = 0.15,
    manual_mttr_hours: float = 0.75,
    engineer_hourly_rate: float = 120.0,
    sla_penalty_per_incident: float = 500.0
) -> dict:
    """
    Computes financial savings formula:
    Loss = Actions * P(hallucination) * (MTTR_manual * Rate + SLA_Penalties)
    """
    total_hallucinated_actions = annual_agent_actions * hallucination_rate
    triage_cost_per_incident = (manual_mttr_hours * engineer_hourly_rate) + sla_penalty_per_incident
    annual_loss_without_graphoath = total_hallucinated_actions * triage_cost_per_incident
    
    # GraphOath guarantees 0 hallucinated writes execute
    annual_loss_with_graphoath = 0.0
    net_savings = annual_loss_without_graphoath - annual_loss_with_graphoath
    
    return {
        "annual_agent_actions": annual_agent_actions,
        "hallucination_rate": f"{hallucination_rate * 100:.1f}%",
        "hallucinated_write_attempts": int(total_hallucinated_actions),
        "triage_cost_per_incident": f"${triage_cost_per_incident:,.2f}",
        "annual_loss_without_graphoath": f"${annual_loss_without_graphoath:,.2f}",
        "annual_loss_with_graphoath": f"${annual_loss_with_graphoath:,.2f}",
        "net_annual_roi_savings": f"${net_savings:,.2f}"
    }

if __name__ == "__main__":
    print("=======================================================================")
    print("GraphOath — Financial Cost of Hallucination ROI Model Demo")
    print("=======================================================================")
    
    results = calculate_hallucination_cost_savings()
    for key, val in results.items():
        print(f"{key.replace('_', ' ').title():<35}: {val}")
        
    print("=======================================================================")
    print("[OK] Financial ROI Model Calculated Successfully.")
