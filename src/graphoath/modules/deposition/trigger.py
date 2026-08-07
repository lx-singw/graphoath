from typing import Dict, Any

class DepositionTrigger:
    def normalize_event(self, raw_payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "event": raw_payload.get("event", "field_removed"),
            "urn": raw_payload.get("urn", "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)"),
            "field": raw_payload.get("field", "customer_region")
        }
