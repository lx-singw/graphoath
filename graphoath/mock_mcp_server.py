"""
GraphOath Zero-Dependency Standalone Mock MCP Server.

Implements Model Context Protocol (MCP) JSON-RPC handlers for DataHub tools
(search_across_lineage, get_dataset_ownership, get_dataset_assertions) over stdio.
"""

import json
import sys
from typing import Dict, Any, List

MOCK_LINEAGE_GRAPH = {
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)": [
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)",
        "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fct_daily_revenue,PROD)"
    ]
}

MOCK_OWNERSHIP = {
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)": "urn:li:corpuser:alice_data_owner",
    "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)": "urn:li:corpuser:bob_data_eng"
}

class MockMCPServer:
    """
    Model Context Protocol (MCP) JSON-RPC Server for DataHub.
    """
    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "search_across_lineage",
                "description": "Trace downstream lineage from dataset URN",
                "parameters": {"type": "object", "properties": {"urn": {"type": "string"}}}
            },
            {
                "name": "get_dataset_ownership",
                "description": "Get owners for dataset URN",
                "parameters": {"type": "object", "properties": {"urn": {"type": "string"}}}
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        urn = arguments.get("urn", "")
        if tool_name == "search_across_lineage":
            downstream = MOCK_LINEAGE_GRAPH.get(urn, [])
            return {"status": "SUCCESS", "downstream_urns": downstream, "count": len(downstream)}
        elif tool_name == "get_dataset_ownership":
            owner = MOCK_OWNERSHIP.get(urn, "urn:li:corpuser:platform_admin")
            return {"status": "SUCCESS", "owner_urn": owner}
        return {"status": "ERROR", "message": f"Unknown tool '{tool_name}'"}

if __name__ == "__main__":
    server = MockMCPServer()
    tools = server.list_tools()
    print(f"[Mock MCP Server] Listed {len(tools)} DataHub tool(s).")
    
    res = server.call_tool("search_across_lineage", {"urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"})
    print(f"[Mock MCP Server Response] {res}")
    assert res["status"] == "SUCCESS"
