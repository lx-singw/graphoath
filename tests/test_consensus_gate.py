import pytest
from graphoath.ops.consensus import MultiAgentConsensusGate, AgentAction

def test_consensus_priority_matrix_incident_blocks_deprecate():
    MultiAgentConsensusGate.clear_locks()
    gate = MultiAgentConsensusGate()
    target = "urn:li:dataset:(snowflake,prod.orders)"

    # 1. Deposition Agent raises Incident (Rank 2)
    act1 = AgentAction(
        action_id="act_inc_1",
        agent_id="agent_deposition_v1",
        action_type="raiseIncident",
        target_urn=target
    )
    res1 = gate.resolve_action_conflict(act1)
    assert res1.approved is True
    assert res1.priority_rank == 2

    # 2. FinOps Agent attempts deprecateDataset (Rank 4)
    act2 = AgentAction(
        action_id="act_dep_1",
        agent_id="agent_finops_v1",
        action_type="deprecateDataset",
        target_urn=target
    )
    res2 = gate.resolve_action_conflict(act2)
    assert res2.approved is False
    assert res2.winning_action_id == "act_inc_1"
    assert "blocked" in res2.reason.lower()
