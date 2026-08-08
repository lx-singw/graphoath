"""
GraphOath Zero-Trust SPIFFE/SPIRE Workload Identity Package
"""

from graphoath.identity.spiffe import SPIFFEWorkloadFetcher, get_workload_identity

__all__ = ["SPIFFEWorkloadFetcher", "get_workload_identity"]
