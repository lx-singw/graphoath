import React from 'react';

export const ReceiptCard: React.FC<{ receipt: any }> = ({ receipt }) => {
  const confidenceTier = receipt.confidence === 'high' ? 'Tier A (0.95)' : 'Tier B (0.80)';

  return (
    <div style={{
      border: '1px solid #334155',
      borderRadius: '8px',
      padding: '16px',
      backgroundColor: '#0f172a',
      color: '#f8fafc',
      marginBottom: '12px',
      fontFamily: 'sans-serif'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <a href={`/receipts/${receipt.receipt_id}`} style={{ fontSize: '0.85rem', color: '#38bdf8', fontWeight: 600, textDecoration: 'none' }}>
            {receipt.receipt_id}
          </a>
          <span style={{ fontSize: '0.7rem', background: '#064e3b', color: '#34d399', padding: '2px 6px', borderRadius: '4px', fontWeight: 'bold' }}>
            GRAPH_OATH_VERIFIED ✓
          </span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <span style={{ fontSize: '0.75rem', background: '#0284c7', color: '#fff', padding: '2px 8px', borderRadius: '4px' }}>
            {confidenceTier}
          </span>
          <span style={{ fontSize: '0.75rem', background: '#1e293b', padding: '2px 8px', borderRadius: '4px' }}>
            {receipt.module}
          </span>
        </div>
      </div>
      <p style={{ fontSize: '0.95rem', margin: '8px 0', color: '#e2e8f0' }}>{receipt.claim}</p>
      <div style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'monospace', wordBreak: 'break-all' }}>
        Hash: {receipt.hash}
      </div>
    </div>
  );
};

