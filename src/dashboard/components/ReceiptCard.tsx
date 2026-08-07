import React from 'react';

export interface ReceiptData {
  receipt_id: str;
  module: string;
  created_at: string;
  claim: string;
  confidence?: string;
  hash: string;
  prev_hash: string;
}

export const ReceiptCard: React.FC<{ receipt: any }> = ({ receipt }) => {
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
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '0.85rem', color: '#38bdf8', fontWeight: 600 }}>{receipt.receipt_id}</span>
        <span style={{ fontSize: '0.75rem', background: '#1e293b', padding: '2px 8px', borderRadius: '4px' }}>
          {receipt.module}
        </span>
      </div>
      <p style={{ fontSize: '0.95rem', margin: '8px 0', color: '#e2e8f0' }}>{receipt.claim}</p>
      <div style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'monospace', wordBreak: 'break-all' }}>
        Hash: {receipt.hash}
      </div>
    </div>
  );
};
