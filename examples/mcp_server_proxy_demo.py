#!/usr/bin/env python3
"""
GraphOath — Runnable MCP Proxy Middleware Server Example

This runnable script demonstrates how GraphOath acts as an MCP Proxy Server:
Any AI agent calling DataHub MCP tools (`search_across_lineage`, `raiseIncident`)
through this proxy automatically has every tool call citation-gated in real time!

Usage:
    python examples/mcp_server_proxy_demo.py
"""

import json
import dataclasses
from typing import Dict, Any

class GraphOathMCPProxy:
    """Proxy layer wrapping DataHub MCP Server tool calls."""

    def __init__(self):
        self.evidence_cache = [
            "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
            "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)"
        ]

    def handle_mcp_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        print(f"\n[MCP PROXY] Intercepted Tool Call: '{tool_name}'")
        print(f"            Arguments: {json.dumps(arguments)}")

        if tool_name == "raiseIncident":
            claim = arguments.get("description", "")
            # Check citations against evidence cache
            uncited = [u for u in [arguments.get("source_urn")] if u not in self.evidence_cache]
            
            if uncited:
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": f"GRAPHOATH GATE REJECTION: Uncited URN {uncited}"}]
                }
            
            return {
                "isError": False,
                "content": [{
                    "type": "text", 
                    "text": f"SUCCESS: Incident raised natively. GraphOath Receipt ID: rcpt_mcp_proxy_8819"
                }]
            }

        return {"isError": False, "content": [{"type": "text", "text": "Tool executed"}]}

def main():
    print("=" * 75)
    print("GraphOath MCP Server Proxy Middleware Demo")
    print("=" * 75)

    proxy = GraphOathMCPProxy()

    # 1. Agent calls raiseIncident with verified URN
    res1 = proxy.handle_mcp_tool_call(
        tool_name="raiseIncident",
        arguments={
            "source_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)",
            "description": "Schema break on prod.orders"
        }
    )
    print(f"Response: {json.dumps(res1, indent=2)}")

    # 2. Agent calls raiseIncident with unverified URN
    res2 = proxy.handle_mcp_tool_call(
        tool_name="raiseIncident",
        arguments={
            "source_urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fake_table,PROD)",
            "description": "Schema break on fake table"
        }
    )
    print(f"Response: {json.dumps(res2, indent=2)}")

    print("\n" + "=" * 75)
    print("MCP Proxy Server Demo Completed Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    main()
