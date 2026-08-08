import pytest
from graphoath.adapters.decorator import graphoath_protected, CitationGateValidationError
from graphoath.custody.ledger import Ledger

@pytest.mark.asyncio
async def test_decorator_rejects_hallucinated_urn():
    @graphoath_protected()
    async def deprecate_dataset_tool(target_urn: str):
        return {"status": "DEPRECATED", "urn": target_urn}

    hallucinated_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.fake_table_99,PROD)"
    
    with pytest.raises(CitationGateValidationError) as exc_info:
        await deprecate_dataset_tool(target_urn=hallucinated_urn)
        
    assert hallucinated_urn in exc_info.value.missing_citations

@pytest.mark.asyncio
async def test_decorator_allows_valid_lineage_urn():
    @graphoath_protected()
    async def deprecate_dataset_tool(target_urn: str):
        return {"status": "DEPRECATED", "urn": target_urn}

    valid_urn = "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.orders,PROD)"
    res = await deprecate_dataset_tool(target_urn=valid_urn)
    
    assert res["status"] == "DEPRECATED"
    assert res["urn"] == valid_urn

    ledger = Ledger()
    all_rcpts = ledger.get_all_receipts()
    assert len(all_rcpts) >= 1
