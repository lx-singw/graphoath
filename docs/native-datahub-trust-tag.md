# GraphOath — Native DataHub Trust Tag & Aspect Specification

This document specifies how **GraphOath** writes lightweight, native trust tags (`GRAPH_OATH_VERIFIED`) directly onto DataHub datasets, making verification visible inside DataHub's native UI without requiring access to the GraphOath dashboard.

---

## 1. Native DataHub UI Trust Tagging

When Deposition completes a citation-gated action on a dataset URN, it calls DataHub GraphQL `addTag` mutation:

- **Tag URN**: `urn:li:tag:GRAPH_OATH_VERIFIED`
- **Tag Description**: *"Verified by GraphOath Citation Gate — Evidence Package Attached"*
- **Color**: Green (`#00C853`)

```
 ┌─────────────────────────────────────────────────────────────┐
 │                    DataHub UI Dataset Page                  │
 │                                                             │
 │  dataset: prod.stg_orders                                   │
 │  Tags: [ Snowflake ] [ dbt ] [ GRAPH_OATH_VERIFIED ✓ ]      │
 └─────────────────────────────────────────────────────────────┘
```

---

## 2. GraphQL Mutation Payload

GraphOath executes the native `addTag` mutation:

```graphql
mutation addGraphOathTrustTag($input: TagAssociationInput!) {
  addTag(input: $input)
}
```

```json
{
  "input": {
    "tagUrn": "urn:li:tag:GRAPH_OATH_VERIFIED",
    "resourceUrn": "urn:li:dataset:(urn:li:dataPlatform:snowflake,prod.stg_orders,PROD)"
  }
}
```

This guarantees that any user or agent browsing DataHub's native UI immediately sees which assets have verified citation receipts attached!
