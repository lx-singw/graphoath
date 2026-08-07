'use client';

import React, { useEffect, useState } from 'react';
import { ReceiptCard } from '../components/ReceiptCard';

export default function OverviewPage() {
  const [receipts, setReceipts] = useState<any[]>([]);

  useEffect(() => {
    fetch('/api/receipts')
      .then((res) => res.json())
      .then((data) => {
        if (data.receipts) setReceipts(data.receipts);
      })
      .catch(() => {
        // Fallback demo state if API offline
        setReceipts([
          {
            receipt_id: 'rcpt_2026-08-05T14:32:07Z-0091',
            module: 'deposition',
            created_at: '2026-08-05T14:32:07Z',
            claim: 'Removing customer_region will affect churn-overview and churn_model_v3',
            hash: '9f2a1e7c3b5d8f0a2c4e6b8d0f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d5f7a',
            prev_hash: '7c11de88f4a2b6c8e0d2f4a6c8e0b2d4f6a8c0e2b4d6f8a0c2e4b6d8f0a2c4e6'
          }
        ]);
      });
  }, []);

  return (
    <div>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>Governance Activity</h2>
      <p style={{ color: '#94a3b8', marginBottom: '24px' }}>Real-time agentic evidence receipts and verification log.</p>

      <div>
        {receipts.map((r) => (
          <ReceiptCard key={r.receipt_id} receipt={r} />
        ))}
      </div>
    </div>
  );
}
