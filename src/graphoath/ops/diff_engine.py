import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from graphoath.datahub.client import DataHubClientWrapper
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger

@dataclass
class DiffReport:
    source_urn: str
    naive_claim_text: str
    naive_urns: List[str]
    verified_claim_text: str
    verified_urns: List[str]
    dropped_hallucinations: List[str]
    blast_radius_saved: int
    citation_resolution_rate: float
    receipt_id: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class NaiveVsVerifiedDiffEngine:
    """
    Engine for simulating and evaluating unconstrained Naive LLM output vs.
    GraphOath Citation-Gated Verified output.
    """
    
    def __init__(self, client: Optional[DataHubClientWrapper] = None):
        self.client = client or DataHubClientWrapper()
        self.ledger = Ledger()

    def run_diff(self, source_urn: str, naive_claim_text: str, naive_urns: List[str]) -> DiffReport:
        evidence_pkg = self.client.get_evidence_package(source_urn, max_hops=3)
        valid_evidence_urns = set(evidence_pkg.lineage_urns)
        valid_evidence_urns.add(source_urn)

        verified_urns = [u for u in naive_urns if u in valid_evidence_urns]
        dropped_hallucinations = [u for u in naive_urns if u not in valid_evidence_urns]

        # Construct verified claim text with hallucinations stripped
        verified_claim_text = naive_claim_text
        for hall in dropped_hallucinations:
            verified_claim_text = verified_claim_text.replace(hall, "[STRIPPED_UNVERIFIED_CITATION]")

        resolution_rate = 1.0 if not naive_urns else round(len(verified_urns) / len(naive_urns), 4)
        blast_radius_saved = len(dropped_hallucinations) * 3  # Estimated 3 downstream systems protected per hallucinated URN

        receipt_id = f"rcpt_diff_{uuid.uuid4().hex[:8]}"
        rcpt = CustodyReceipt(
            receipt_id=receipt_id,
            action_type="naive_vs_verified_diff",
            target_urn=source_urn,
            evidence_payload=[{"urn": u} for u in valid_evidence_urns],
            claims_payload={
                "naive_claim": naive_claim_text,
                "naive_urns": naive_urns,
                "dropped_hallucinations": dropped_hallucinations
            },
            gate_decision="APPROVED" if not dropped_hallucinations else "PARTIALLY_REDACTED",
            confidence_score=resolution_rate
        )
        self.ledger.append_custody_receipt(rcpt)

        return DiffReport(
            source_urn=source_urn,
            naive_claim_text=naive_claim_text,
            naive_urns=naive_urns,
            verified_claim_text=verified_claim_text,
            verified_urns=verified_urns,
            dropped_hallucinations=dropped_hallucinations,
            blast_radius_saved=blast_radius_saved,
            citation_resolution_rate=resolution_rate,
            receipt_id=receipt_id
        )
