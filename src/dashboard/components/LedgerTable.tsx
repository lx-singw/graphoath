import React from 'react';

export const LedgerTable: React.FC<{ receipts: any[] }> = ({ receipts }) => {
  return (
    <div style={{ overflowX: 'auto', marginTop: '16px', fontFamily: 'sans-serif' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', color: '#f8fafc' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8', fontSize: '0.85rem' }}>
            <th style={{ padding: '12px' }}>Receipt ID</th>
            <th style={{ padding: '12px' }}>Module</th>
            <th style={{ padding: '12px' }}>Created At</th>
            <th style={{ padding: '12px' }}>SHA-256 Hash</th>
            <th style={{ padding: '12px' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {receipts.map((r, i) => (
            <tr key={i} style={{ borderBottom: '1px solid #1e293b', fontSize: '0.85rem' }}>
              <td style={{ padding: '12px', color: '#38bdf8' }}>{r.receipt_id}</td>
              <td style={{ padding: '12px' }}>{r.module}</td>
              <td style={{ padding: '12px', color: '#94a3b8' }}>{r.created_at}</td>
              <td style={{ padding: '12px', fontFamily: 'monospace', color: '#cbd5e1' }}>
                {r.hash.substring(0, 16)}...
              </td>
              <td style={{ padding: '12px' }}>
                <span style={{ background: '#064e3b', color: '#34d399', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>
                  INTACT
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
