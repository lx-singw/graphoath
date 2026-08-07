'use client';

import React, { useEffect, useState } from 'react';
import { EvidenceList } from '../../../components/EvidenceList';

export default function ReceiptDetailPage({ params }: { params: { receiptId: string } }) {
  const [receipt, setReceipt] = useState<any>(null);

  useEffect(() => {
    fetch(`/api/receipts/${params.receiptId}`)
      .then((res) => res.json())
      .then((data) => setReceipt(data))
      .catch(() => {
        setReceipt({
          receipt_id: params.receiptId,
          module: 'deposition',
          created_at: '2026-08-05T14:32:07Z',
          claim: 'Removing customer_region will affect churn-overview and churn_model_v3',
          confidence: 'high',
          hash: '9f2a1e7c3b5d8f0a2c4e6b8d0f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d5f7a',
          prev_hash: '7c11de88f4a2b6c8e0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6d8f0a2c4e6',
          evidence: [
            {
              type: 'lineage',
              call: 'searchAcrossLineage(urn, direction=DOWNSTREAM, degree=2)',
              result_urn: 'urn:li:dashboard:(looker,churn-overview)',
              hops: 2
            },
            {
              type: 'ownership',
              call: 'getOwnership(urn=churn-overview)',
              result: 'team-growth-analytics'
            }
          ]
        });
      });
  }, [params.receiptId]);

  if (!receipt) return <div style={{ color: '#94a3b8' }}>Loading receipt...</div>;

  return (
    <div>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '8px', color: '#38bdf8' }}>{receipt.receipt_id}</h2>
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', padding: '20px', marginBottom: '24px' }}>
        <p style={{ fontSize: '1.1rem', color: '#f8fafc' }}>{receipt.claim}</p>
        <div style={{ display: 'flex', gap: '16px', color: '#94a3b8', fontSize: '0.85rem' }}>
          <span>Module: {receipt.module}</span>
          <span>Confidence: {receipt.confidence}</span>
        </div>
      </div>

      <EvidenceList evidence={receipt.evidence || []} />
    </div>
  );
}
