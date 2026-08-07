# DataHub Community PR & Contribution Guide: GraphOath Receipt Aspect

This document details the step-by-step contribution path for upstreaming the `graphoathReceipt` aspect into the official open-source **`datahub-project/datahub`** repository.

---

## 1. Upstream Aspect Target Location

To integrate GraphOath's citation receipt aspect directly into DataHub GMS (DataHub Metadata Service):

1. **Avro Schema Placement**:
   Place [`schemas/graphoathReceipt.avsc`](schemas/graphoathReceipt.avsc) into:
   `metadata-models/src/main/resources/mcr/aspects/com/linkedin/dataset/graphoathReceipt.avsc`

2. **Aspect Annotation**:
   Annotate the aspect with `@Aspect(name = "graphoathReceipt")` to generate GraphQL queries and GMS search indexing automatically.

---

## 2. Pull Request Checklist for `datahub-project/datahub`

- [x] **Pegasus Avro Schema Definition**: Validated against Pegasus Gradle build tools.
- [x] **Entity Binding**: Attached to `dataset`, `incident`, and `chart` entity types in `entity-registry.yaml`.
- [x] **GraphQL Mutations**: Supported via `emitMetadataChangeProposal`.
- [x] **Documentation**: Includes JSON schema payload examples.

---

## 3. RFC Specification Link

For complete details on the citation gate pattern, see [`docs/datahub-rfc-citation-gate.md`](docs/datahub-rfc-citation-gate.md).
