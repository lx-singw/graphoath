# GraphOath — Custody Ledger Disaster Recovery & S3 WORM Mirroring

This document specifies **GraphOath's Disaster Recovery Architecture** and cloud object storage mirroring protocol for the Custody Ledger.

---

## 1. Cloud Object Lock (WORM) Architecture

While primary receipt persistence lives in PostgreSQL, high-compliance environments require mirroring to **Write Once Read Many (WORM)** cloud storage:

```
  Postgres Custody Ledger               AWS S3 / GCS WORM Storage
 ┌───────────────────────┐             ┌─────────────────────────┐
 │ Receipt 1402          │             │ S3 Object Lock          │
 │ SHA-256 Hash Chain    ├────────────►│ Compliance Mode         │
 └───────────────────────┘             │ (Retain 7 Years)        │
                                       └─────────────────────────┘
```

---

## 2. Disaster Recovery Protocol

If the primary PostgreSQL database experiences hardware failure, corruption, or malicious wipeout:

1. **Reconstruction from S3**: Custody receipts are restored from immutable S3 Compliance Mode storage.
2. **Chain Re-Verification**: `python -m graphoath.db.verify_ledger` recomputes the SHA-256 hash chain from genesis receipt `#0` to head.
3. **DataHub Aspect Cross-Validation**: Restored receipts are cross-referenced against `graphoathReceipt` aspects stored on live DataHub entities.
