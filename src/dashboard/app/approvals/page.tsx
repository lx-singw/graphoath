'use client';

import React, { useState } from 'react';

export default function ApprovalsPage() {
  const [pendingApprovals, setPendingApprovals] = useState([
    {
      id: 'act_pause_dbt_stg_orders_001',
      action: 'PAUSE_MODEL_EXECUTION',
      target_urn: 'urn:li:dataset:(dbt,dbt.stg_orders,PROD)',
      risk_level: 'MEDIUM_REQUIRES_APPROVAL',
      agent: 'deposition_agent_v1',
      details: 'Generates dbt --defer payload to pause stg_orders model execution during CI runs.'
    }
  ]);

  const handleAction = (id: string, action: 'approve' | 'deny') => {
    setPendingApprovals((prev) => prev.filter((item) => item.id !== id));
    alert(`Action ${id} successfully ${action}d!`);
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', margin: 0, fontWeight: 700 }}>Human-in-the-Loop (HITL) Approval Queue</h2>
        <p style={{ color: '#94a3b8', margin: '4px 0 0 0' }}>Review and approve/deny pending automated remediation playbooks and sensitive governance actions.</p>
      </div>

      {pendingApprovals.length === 0 ? (
        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '48px', textAlign: 'center' }}>
          <span style={{ fontSize: '2rem' }}>🎉</span>
          <h3 style={{ color: '#f8fafc', margin: '8px 0 0 0' }}>Queue Clean — No Pending Approvals</h3>
          <p style={{ color: '#64748b', fontSize: '0.875rem' }}>All automated remediation actions are either auto-executed or approved.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {pendingApprovals.map((item) => (
            <div key={item.id} style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                <div>
                  <span style={{ background: '#7c2d12', color: '#fdba74', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem', fontWeight: 600 }}>
                    {item.risk_level}
                  </span>
                  <h3 style={{ margin: '8px 0 0 0', fontSize: '1.125rem', color: '#f8fafc' }}>{item.action}</h3>
                </div>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    onClick={() => handleAction(item.id, 'approve')}
                    style={{ background: '#166534', color: '#4ade80', border: 'none', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer', fontWeight: 600 }}
                  >
                    ✓ Approve
                  </button>
                  <button
                    onClick={() => handleAction(item.id, 'deny')}
                    style={{ background: '#991b1b', color: '#fca5a5', border: 'none', padding: '8px 16px', borderRadius: '6px', cursor: 'pointer', fontWeight: 600 }}
                  >
                    ✗ Deny
                  </button>
                </div>
              </div>

              <p style={{ color: '#cbd5e1', fontSize: '0.875rem', margin: '0 0 12px 0' }}>{item.details}</p>
              <div style={{ fontSize: '0.75rem', color: '#64748b', fontFamily: 'monospace' }}>
                Target URN: {item.target_urn} | Agent: {item.agent}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
