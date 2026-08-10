from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/calculator", tags=["Financial Calculator"])

class CalculatorInput(BaseModel):
    team_size: int = 20
    downtime_hourly_rate: float = 12000.0
    engineering_hourly_rate: float = 150.0

class CalculatorResult(BaseModel):
    legacy_monthly_cost: float
    un_gated_ai_monthly_cost: float
    graphoath_monthly_cost: float
    monthly_savings: float
    annual_savings: float
    cost_reduction_percent: float

@router.post("/roi", response_model=CalculatorResult)
async def calculate_roi(body: CalculatorInput):
    # Calculations based on docs/cost-of-hallucination-calculator.md model
    downtime_hours_legacy = 12.0
    downtime_hours_ungated = 18.0
    downtime_hours_graphoath = 0.5

    triage_hours_legacy = 360.0
    triage_hours_ungated = 240.0
    triage_hours_graphoath = 10.0

    legacy_cost = (downtime_hours_legacy * body.downtime_hourly_rate) + (triage_hours_legacy * body.engineering_hourly_rate)
    ungated_cost = (downtime_hours_ungated * body.downtime_hourly_rate) + (triage_hours_ungated * body.engineering_hourly_rate) + 2160.0
    graphoath_cost = (downtime_hours_graphoath * body.downtime_hourly_rate) + (triage_hours_graphoath * body.engineering_hourly_rate)

    monthly_savings = ungated_cost - graphoath_cost
    annual_savings = monthly_savings * 12.0
    reduction_percent = round(((ungated_cost - graphoath_cost) / ungated_cost) * 100.0, 1)

    return CalculatorResult(
        legacy_monthly_cost=legacy_cost,
        un_gated_ai_monthly_cost=ungated_cost,
        graphoath_monthly_cost=graphoath_cost,
        monthly_savings=monthly_savings,
        annual_savings=annual_savings,
        cost_reduction_percent=reduction_percent
    )
