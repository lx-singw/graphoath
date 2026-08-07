# GraphOath — Judge-Runnable Independent Receipt Verifier Guide

This guide explains how hackathon judges can independently verify the cryptographic SHA-256 hash chains of GraphOath Custody receipts using a standalone zero-dependency script.

---

## 1. Zero-Trust Verification Concept

Instead of asking judges to "watch us catch a tampered record" or trust static screenshots, GraphOath provides a **Judge-Runnable Independent Verifier Script**.

Judges do **not** need:
- Docker running
- A local DataHub instance
- Python dependencies beyond standard library

---

## 2. Running the Independent Verifier

Run the verifier script from the repository root:

```bash
python examples/verify_receipt_chain.py
```

### What the Verifier Performs:
1. Loads exported Custody receipt JSON payloads from `examples/`.
2. Extracts receipt parameters (`timestamp`, `evidence_package`, `action_executed`, `prev_hash`).
3. Re-computes SHA-256 hash signatures from genesis.
4. Checks stored `receipt_hash` against recomputed hash values.

---

## 3. Expected Output

```
===========================================================================
GraphOath Independent Receipt Chain Cryptographic Verifier
===========================================================================

[1] Found 2 exported Custody receipt files:
    - examples/receipt-schema-break.json
    - examples/receipt-repeat-incident.json

[2] Re-computing SHA-256 Hash Chains Independently...

    Evaluating Receipt: rcpt_98f4a12b-7c3e-4b9d-a8f1-2e6b5c4d3a01
    - Stored Hash : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    - Status      : [OK] Cryptographically Valid SHA-256 Hash Signature!

===========================================================================
INDEPENDENT AUDIT RESULT: 2/2 Receipts Verified Intact.
===========================================================================
```
