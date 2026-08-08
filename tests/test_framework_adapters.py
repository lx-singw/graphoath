import pytest
from graphoath.adapters.langchain_adapter import GraphOathIncidentTool, GraphOathCitationToolWrapper
from graphoath.adapters.llamaindex_adapter import llama_graphoath_protected, LlamaIndexGraphOathPostProcessor
from graphoath.adapters.adk_adapter import GraphOathADKInterceptor
from graphoath.adapters.decorator import CitationGateValidationError

def test_langchain_incident_tool():
    tool = GraphOathIncidentTool()
    source_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    evidence_urns = ["urn:li:dataset:(urn:li:dataPlatform:dbt,dbt.stg_orders,PROD)"]
    
    res = tool._run(
        claim_text="Schema break detected",
        evidence_urns=evidence_urns,
        source_urn=source_urn
    )
    assert "status" in res or "incident_urn" in res

def test_llamaindex_protected_decorator():
    @llama_graphoath_protected()
    def query_tool(target_urn: str):
        return f"Queried {target_urn}"

    valid_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    assert query_tool(target_urn=valid_urn) == f"Queried {valid_urn}"

    fake_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fake_table_123,PROD)"
    with pytest.raises(CitationGateValidationError):
        query_tool(target_urn=fake_urn)

def test_adk_interceptor():
    interceptor = GraphOathADKInterceptor(agent_name="TestADKAgent")
    
    def raw_tool(dataset_urn: str):
        return f"Updated {dataset_urn}"

    valid_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    res = interceptor.intercept_tool_execution(raw_tool, {"dataset_urn": valid_urn})
    assert res == f"Updated {valid_urn}"

    fake_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fake_table_456,PROD)"
    with pytest.raises(CitationGateValidationError):
        interceptor.intercept_tool_execution(raw_tool, {"dataset_urn": fake_urn})
