import os
import pytest
from unittest.mock import patch
from graphoath.identity.spiffe import SPIFFEIdentityVerifier, SPIFFEWorkloadFetcher

def test_validate_spiffe_svid_valid():
    verifier = SPIFFEIdentityVerifier()
    header_val = "spiffe://graphoath.io/agent/deposition-v1"
    parsed = verifier.parse_svid_header(header_val)
    
    assert parsed["spiffe_id"] == "spiffe://graphoath.io/agent/deposition-v1"
    assert parsed["agent_name"] == "deposition-v1"
    assert verifier.verify_identity(header_val) is True

def test_reject_expired_or_invalid_svid():
    verifier = SPIFFEIdentityVerifier()
    invalid_header = "ab"  # Too short / invalid format
    assert verifier.verify_identity(invalid_header) is False
