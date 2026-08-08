import time
from typing import Dict, Any, List, Optional, Set
from pydantic import BaseModel

ACTION_PRIORITY_RANK = {
    # Rank 1 (Highest): Security & Regulatory Containment
    "quarantineDataset": 1,
    "revokeAccess": 1,
    
    # Rank 2: Incident Triage & Alerting
    "raiseIncident": 2,
    "updateIncident": 2,
    "addTag": 2,
    
    # Rank 3: Active Pipeline Read
    "readQuery": 3,
    "featureExtraction": 3,
    
    # Rank 4 (Lowest): Cost Optimization & Pruning
    "deprecateDataset": 4,
    "dropColumn": 4,
    "deleteTag": 4
}

class AgentAction(BaseModel):
    action_id: str
    agent_id: str
    action_type: str
    target_urn: str
    timestamp: float = 0.0
    signatures: List[str] = []

    def model_post_init(self, __context: Any) -> None:
        if not self.timestamp:
            self.timestamp = time.time()

class ConsensusDecision(BaseModel):
    approved: bool
    reason: str
    winning_action_id: str
    priority_rank: int
    active_locks: List[str]

class MultiAgentConsensusGate:
    """
    Multi-Agent Consensus Conflict Resolution Gate:
    Enforces Priority Ranks 1-4 across concurrent agent tool calls targeting the same dataset URN.
    """
    _urn_session_locks: Dict[str, List[AgentAction]] = {}

    @classmethod
    def clear_locks(cls):
        cls._urn_session_locks.clear()

    def __init__(self, required_signatures_for_destructive: int = 1):
        self.required_signatures = required_signatures_for_destructive

    def register_action(self, action: AgentAction) -> ConsensusDecision:
        return self.resolve_action_conflict(action)

    def resolve_action_conflict(self, proposed_action: AgentAction) -> ConsensusDecision:
        urn = proposed_action.target_urn
        proposed_rank = ACTION_PRIORITY_RANK.get(proposed_action.action_type, 4)

        if urn not in MultiAgentConsensusGate._urn_session_locks:
            MultiAgentConsensusGate._urn_session_locks[urn] = []

        active_actions = MultiAgentConsensusGate._urn_session_locks[urn]

        # 1. Check for higher priority existing locks
        for existing in active_actions:
            existing_rank = ACTION_PRIORITY_RANK.get(existing.action_type, 4)

            # Rule: Higher rank (lower rank number) overrides lower rank
            if existing_rank < proposed_rank:
                # E.g., Rank 2 (raiseIncident) blocks Rank 4 (deprecateDataset)
                reason = (
                    f"Action '{proposed_action.action_type}' (Rank {proposed_rank}) blocked on '{urn}' "
                    f"by active higher-priority action '{existing.action_type}' (Rank {existing_rank})."
                )
                return ConsensusDecision(
                    approved=False,
                    reason=reason,
                    winning_action_id=existing.action_id,
                    priority_rank=existing_rank,
                    active_locks=[a.action_id for a in active_actions]
                )

            # Rule: Rank 3 active reads prevent Rank 4 deprecation
            if existing_rank == 3 and proposed_rank == 4:
                reason = (
                    f"Deprecation action '{proposed_action.action_type}' blocked on '{urn}' "
                    f"due to active pipeline read lock '{existing.action_type}'."
                )
                return ConsensusDecision(
                    approved=False,
                    reason=reason,
                    winning_action_id=existing.action_id,
                    priority_rank=3,
                    active_locks=[a.action_id for a in active_actions]
                )

        # 2. Quorum check for destructive action
        if proposed_rank == 4 and len(proposed_action.signatures) < self.required_signatures:
            reason = (
                f"Destructive action '{proposed_action.action_type}' requires {self.required_signatures} agent "
                f"signatures, but only {len(proposed_action.signatures)} provided."
            )
            return ConsensusDecision(
                approved=False,
                reason=reason,
                winning_action_id=proposed_action.action_id,
                priority_rank=proposed_rank,
                active_locks=[a.action_id for a in active_actions]
            )

        # 3. If proposed action has higher priority than existing lower priority actions, purge lower priority actions
        MultiAgentConsensusGate._urn_session_locks[urn] = [
            a for a in active_actions if ACTION_PRIORITY_RANK.get(a.action_type, 4) <= proposed_rank
        ]
        MultiAgentConsensusGate._urn_session_locks[urn].append(proposed_action)

        return ConsensusDecision(
            approved=True,
            reason=f"Action '{proposed_action.action_type}' (Rank {proposed_rank}) granted consensus lock on '{urn}'.",
            winning_action_id=proposed_action.action_id,
            priority_rank=proposed_rank,
            active_locks=[a.action_id for a in MultiAgentConsensusGate._urn_session_locks[urn]]
        )
