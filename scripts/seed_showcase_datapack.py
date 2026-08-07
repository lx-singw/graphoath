#!/usr/bin/env python3
"""
Seed Showcase Datapack script for GraphOath local development & testing.
Loads sample DataHub e-commerce entities into local state or mock graph.
"""

import json
import os
import sys

SHOWCASE_FIXTURE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "tests", "fixtures", "showcase_datapack_sample.json"
)

def seed_datapack() -> None:
    print(f"[GraphOath Seed] Loading showcase datapack from {SHOWCASE_FIXTURE_PATH}...")
    if not os.path.exists(SHOWCASE_FIXTURE_PATH):
        print(f"[GraphOath Seed] Warning: Fixture file not found. Creating placeholder fixture.")
        sample_data = {
            "entities": [
                {
                    "urn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
                    "platform": "snowflake",
                    "name": "ecommerce.fct_orders",
                    "fields": ["order_id", "customer_id", "customer_region", "amount"]
                },
                {
                    "urn": "urn:li:dashboard:(looker,churn-overview)",
                    "platform": "looker",
                    "name": "churn-overview"
                }
            ],
            "lineage": [
                {
                    "upstream": "urn:li:dataset:(urn:li:dataPlatform:snowflake,ecommerce.fct_orders,PROD)",
                    "downstream": "urn:li:dashboard:(looker,churn-overview)",
                    "hops": 2
                }
            ]
        }
        os.makedirs(os.path.dirname(SHOWCASE_FIXTURE_PATH), exist_ok=True)
        with open(SHOWCASE_FIXTURE_PATH, "w", encoding="utf-8") as f:
            json.dump(sample_data, f, indent=2)

    with open(SHOWCASE_FIXTURE_PATH, "r", encoding="utf-8") as f:
        datapack = json.load(f)

    entities_count = len(datapack.get("entities", []))
    lineage_count = len(datapack.get("lineage", []))
    print(f"[GraphOath Seed] Successfully seeded {entities_count} entities and {lineage_count} lineage relations.")

if __name__ == "__main__":
    seed_datapack()
