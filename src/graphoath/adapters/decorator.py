import re
import functools
import inspect
import asyncio
from typing import Callable, Any, List, Dict, Optional, Set
from graphoath.custody.receipt import CustodyReceipt
from graphoath.custody.ledger import Ledger
from graphoath.datahub.lineage import get_evidence_package
from graphoath.datahub.client import DataHubClientWrapper

URN_REGEX = re.compile(r"urn:li:[a-zA-Z0-9_]+:\([^)]+\)|urn:li:[a-zA-Z0-9_]+:[a-zA-Z0-9_.-]+")

class CitationGateValidationError(Exception):
    """Raised when an AI agent claim or tool call refers to unverified URNs."""
    def __init__(self, message: str, missing_citations: List[str]):
        super().__init__(message)
        self.missing_citations = missing_citations

def extract_urns_from_obj(obj: Any) -> Set[str]:
    """Recursively extracts all DataHub URN strings from args, kwargs, or data structures."""
    urns = set()
    if isinstance(obj, str):
        matches = URN_REGEX.findall(obj)
        urns.update(matches)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            urns.update(extract_urns_from_obj(item))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            urns.update(extract_urns_from_obj(k))
            urns.update(extract_urns_from_obj(v))
    return urns

def graphoath_protected(
    module: str = "Deposition",
    required_confidence: float = 0.90,
    auto_raise_incident: bool = True
) -> Callable:
    """
    Universal GraphOath protection decorator for AI agent tool functions.
    Enforces Citation-Gated Control Plane policy before executing write actions.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            claimed_urns = set()
            for arg in args:
                claimed_urns.update(extract_urns_from_obj(arg))
            for k, v in kwargs.items():
                claimed_urns.update(extract_urns_from_obj(v))

            target_urn = next(iter(claimed_urns), "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")

            # Fetch evidence lineage
            client = DataHubClientWrapper()
            evidence_pkg = client.get_evidence_package(target_urn, max_hops=3)
            evidence_urns = set(evidence_pkg.lineage_urns)

            # Check citation gate: Claimed URNs must be subset of Evidence URNs
            missing_citations = [u for u in claimed_urns if u not in evidence_urns]
            if missing_citations:
                raise CitationGateValidationError(
                    f"[GraphOath Citation Gate REJECTED] Unverified URN citations: {missing_citations}",
                    missing_citations=missing_citations
                )

            # Execute tool function
            if inspect.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            # Append custody receipt
            ledger = Ledger()
            receipt = CustodyReceipt(
                receipt_id=f"rcpt_dec_{int(asyncio.get_event_loop().time()*1000)}",
                action_type=func.__name__,
                target_urn=target_urn,
                evidence_payload=[{"urn": u} for u in evidence_urns],
                claims_payload={"claimed_urns": list(claimed_urns), "kwargs": str(kwargs)},
                gate_decision="APPROVED",
                confidence_score=required_confidence
            )
            ledger.append_custody_receipt(receipt)

            return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            claimed_urns = set()
            for arg in args:
                claimed_urns.update(extract_urns_from_obj(arg))
            for k, v in kwargs.items():
                claimed_urns.update(extract_urns_from_obj(v))

            target_urn = next(iter(claimed_urns), "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)")

            client = DataHubClientWrapper()
            evidence_pkg = client.get_evidence_package(target_urn, max_hops=3)
            evidence_urns = set(evidence_pkg.lineage_urns)

            missing_citations = [u for u in claimed_urns if u not in evidence_urns]
            if missing_citations:
                raise CitationGateValidationError(
                    f"[GraphOath Citation Gate REJECTED] Unverified URN citations: {missing_citations}",
                    missing_citations=missing_citations
                )

            result = func(*args, **kwargs)

            ledger = Ledger()
            receipt = CustodyReceipt(
                receipt_id=f"rcpt_dec_sync",
                action_type=func.__name__,
                target_urn=target_urn,
                evidence_payload=[{"urn": u} for u in evidence_urns],
                claims_payload={"claimed_urns": list(claimed_urns)},
                gate_decision="APPROVED",
                confidence_score=required_confidence
            )
            ledger.append_custody_receipt(receipt)
            return result

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
