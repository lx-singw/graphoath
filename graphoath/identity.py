"""
GraphOath Agent Identity & Cryptographic Signature Verification Module.

Validates digital signatures attached to agent claim payloads to guarantee non-repudiation.
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Tuple

def sign_agent_claim(secret_key: str, agent_id: str, claim_payload: Dict[str, Any]) -> str:
    """Signs an agent claim payload using HMAC-SHA256."""
    canonical_json = json.dumps(claim_payload, sort_keys=True, separators=(',', ':'))
    to_sign = f"{agent_id}:{canonical_json}".encode('utf-8')
    return hmac.new(secret_key.encode('utf-8'), to_sign, hashlib.sha256).hexdigest()

def verify_agent_claim_signature(
    secret_key: str,
    agent_id: str,
    claim_payload: Dict[str, Any],
    provided_signature: str
) -> Tuple[bool, str]:
    """Verifies that an agent claim payload signature matches the expected HMAC-SHA256 signature."""
    expected_signature = sign_agent_claim(secret_key, agent_id, claim_payload)
    if hmac.compare_digest(expected_signature, provided_signature):
        return True, f"[GraphOath Identity PASSED] Valid digital signature for agent '{agent_id}'."
    return False, f"[GraphOath Identity REJECTED] Signature mismatch for agent '{agent_id}'!"

if __name__ == "__main__":
    key = "secret_agent_key_123"
    agent = "agent_deposition_v1"
    payload = {"target_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)", "action": "raiseIncident"}
    
    sig = sign_agent_claim(key, agent, payload)
    print(f"Generated Signature: {sig}")
    
    is_valid, msg = verify_agent_claim_signature(key, agent, payload, sig)
    print(msg)
    assert is_valid
