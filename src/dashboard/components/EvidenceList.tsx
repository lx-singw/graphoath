import React from 'react';

export const EvidenceList: React.FC<{ evidence: any[] }> = ({ evidence }) => {
  return (
    <div style={{ marginTop: '16px', fontFamily: 'sans-serif' }}>
      <h3 style={{ fontSize: '1rem', color: '#94a3b8', marginBottom: '12px' }}>Evidence Chain ({evidence.length} items)</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {evidence.map((item, idx) => (
          <div key={idx} style={{
            background: '#1e293b',
            borderLeft: '4px solid #38bdf8',
            padding: '12px',
            borderRadius: '4px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '0.8rem' }}>
              <span style={{ textTransform: 'uppercase', fontWeight: 'bold' }}>{item.type}</span>
              {item.hops && <span>Hops: {item.hops}</span>}
            </div>
            <div style={{ fontSize: '0.85rem', color: '#f1f5f9', marginTop: '4px', fontFamily: 'monospace' }}>
              {item.call}
            </div>
            <div style={{ fontSize: '0.8rem', color: '#cbd5e1', marginTop: '4px' }}>
              Result: {item.result_urn || item.result}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
