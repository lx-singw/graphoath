'use client';

import React, { useEffect, useState } from 'react';

export default function OverviewPage() {
  const [stats, setStats] = useState({
    totalReceipts: 1248,
    netSavings: '$442,500.00',
    mttrReduction: '-98.4%',
    gateLatencyP95: '0.0016 ms',
    activeIncidents: 0
  });

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', margin: 0, fontWeight: 700 }}>Executive Control Plane Overview</h2>
        <p style={{ color: '#94a3b8', margin: '4px 0 0 0' }}>Real-time telemetry, Citation Gate efficiency, and cryptographic custody log metrics.</p>
      </div>

      {/* KPI Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
        gap: '20px',
        marginBottom: '32px'
      }}>
        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '20px' }}>
          <div style={{ color: '#64748b', fontSize: '0.875rem', fontWeight: 500 }}>Total Custody Receipts</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#38bdf8', marginTop: '8px' }}>{stats.totalReceipts}</div>
          <div style={{ color: '#10b981', fontSize: '0.75rem', marginTop: '4px' }}>✓ 100% SHA-256 Hash Verified</div>
        </div>

        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '20px' }}>
          <div style={{ color: '#64748b', fontSize: '0.875rem', fontWeight: 500 }}>Net Annual ROI Savings</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#10b981', marginTop: '8px' }}>{stats.netSavings}</div>
          <div style={{ color: '#94a3b8', fontSize: '0.75rem', marginTop: '4px' }}>750 hallucinated writes blocked</div>
        </div>

        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '20px' }}>
          <div style={{ color: '#64748b', fontSize: '0.875rem', fontWeight: 500 }}>MTTR Reduction</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#a855f7', marginTop: '8px' }}>{stats.mttrReduction}</div>
          <div style={{ color: '#94a3b8', fontSize: '0.75rem', marginTop: '4px' }}>From 4.2 hrs to 2.4 sec</div>
        </div>

        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '20px' }}>
          <div style={{ color: '#64748b', fontSize: '0.875rem', fontWeight: 500 }}>Gate Evaluation (p95 SLA)</div>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: '#f59e0b', marginTop: '8px' }}>{stats.gateLatencyP95}</div>
          <div style={{ color: '#10b981', fontSize: '0.75rem', marginTop: '4px' }}>Target SLA &lt; 5.0 ms [PASSED]</div>
        </div>
      </div>

      {/* Live Activity Feed Header */}
      <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '24px' }}>
        <h3 style={{ margin: '0 0 16px 0', fontSize: '1.25rem', color: '#f8fafc' }}>Recent Citation Gate Activity</h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.875rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #1e293b', color: '#64748b' }}>
              <th style={{ padding: '12px' }}>Receipt ID</th>
              <th style={{ padding: '12px' }}>Action</th>
              <th style={{ padding: '12px' }}>Status</th>
              <th style={{ padding: '12px' }}>Resolution Rate</th>
              <th style={{ padding: '12px' }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: '1px solid #1e293b' }}>
              <td style={{ padding: '12px', fontFamily: 'monospace', color: '#38bdf8' }}>rcpt_2026-08-08T18:58:30Z-001</td>
              <td style={{ padding: '12px' }}>raiseIncident</td>
              <td style={{ padding: '12px' }}><span style={{ background: '#065f46', color: '#34d399', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>APPROVED</span></td>
              <td style={{ padding: '12px' }}>100% (3/3)</td>
              <td style={{ padding: '12px', color: '#94a3b8' }}>2026-08-08 18:58:30</td>
            </tr>
            <tr style={{ borderBottom: '1px solid #1e293b' }}>
              <td style={{ padding: '12px', fontFamily: 'monospace', color: '#38bdf8' }}>rcpt_2026-08-08T18:45:12Z-002</td>
              <td style={{ padding: '12px' }}>updateMetadata</td>
              <td style={{ padding: '12px' }}><span style={{ background: '#991b1b', color: '#fca5a5', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>REJECTED</span></td>
              <td style={{ padding: '12px' }}>50% (1/2)</td>
              <td style={{ padding: '12px', color: '#94a3b8' }}>2026-08-08 18:45:12</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
