import os
import pytest
from unittest.mock import patch
from graphoath.identity.spiffe import SPIFFEWorkloadFetcher, get_workload_identity

def test_spiffe_fetcher_default():
    fetcher = SPIFFEWorkloadFetcher()
    ident = fetcher.fetch_svid()
    assert ident["spiffe_id"] == "spiffe://graphoath.io/agent/deposition-v1"
    assert ident["svid_serial"] == "svid-serial-0001"

def test_spiffe_fetcher_env_override():
    with patch.dict(os.environ, {"SPIFFE_ID": "spiffe://example.org/my-agent", "SVID_SERIAL": "svid-1234"}):
        ident = get_workload_identity()
        assert ident["spiffe_id"] == "spiffe://example.org/my-agent"
        assert ident["svid_serial"] == "svid-1234"
        assert ident["source"] == "ENVIRONMENT_SVID"
