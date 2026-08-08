'use client';

import React from 'react';

export default function DiffPage() {
  const naiveClaim = {
    agent_action: "raiseIncident",
    target_urn: "urn:li:dataset:(snowflake,prod.orders)",
    cited_downstream_urns: [
      "urn:li:dataset:(dbt,dbt.stg_orders)",
      "urn:li:dataset:(dbt,dbt.fct_daily_revenue)",
      "urn:li:dataset:(snowflake,prod.hallucinated_marketing_metrics)" // Hallucinated URN!
    ],
    blast_radius_nodes: 3
  };

  const verifiedClaim = {
    agent_action: "raiseIncident",
    target_urn: "urn:li:dataset:(snowflake,prod.orders)",
    cited_downstream_urns: [
      "urn:li:dataset:(dbt,dbt.stg_orders)",
      "urn:li:dataset:(dbt,dbt.fct_daily_revenue)"
    ],
    blast_radius_nodes: 2
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', margin: 0, fontWeight: 700 }}>Naive vs. Verified Claim Diff Viewer</h2>
        <p style={{ color: '#94a3b8', margin: '4px 0 0 0' }}>Side-by-side comparison highlighting unevidenced hallucinated URNs intercepted and stripped by the Citation Gate.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Naive Claim Panel */}
        <div style={{ background: '#0f172a', border: '1px solid #991b1b', borderRadius: '12px', padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ margin: 0, color: '#fca5a5', fontSize: '1.125rem' }}>❌ Naive LLM Claim (Unchecked)</h3>
            <span style={{ background: '#7f1d1d', color: '#fca5a5', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>3 URNs</span>
          </div>
          <pre style={{ background: '#020617', border: '1px solid #1e293b', padding: '16px', borderRadius: '8px', overflowX: 'auto', fontSize: '0.8125rem', color: '#cbd5e1' }}>
{JSON.stringify(naiveClaim, null, 2)}
          </pre>
          <div style={{ background: '#450a0a', padding: '12px', borderRadius: '6px', marginTop: '16px', color: '#fca5a5', fontSize: '0.8125rem' }}>
            ⚠️ Contains 1 hallucinated URN: <code>prod.hallucinated_marketing_metrics</code>. Writing this claim unverified would pollute DataHub search.
          </div>
        </div>

        {/* Verified Claim Panel */}
        <div style={{ background: '#0f172a', border: '1px solid #065f46', borderRadius: '12px', padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ margin: 0, color: '#6ee7b7', fontSize: '1.125rem' }}>🛡️ GraphOath Verified Claim</h3>
            <span style={{ background: '#064e3b', color: '#6ee7b7', padding: '2px 8px', borderRadius: '4px', fontSize: '0.75rem' }}>2 URNs Verified</span>
          </div>
          <pre style={{ background: '#020617', border: '1px solid #1e293b', padding: '16px', borderRadius: '8px', overflowX: 'auto', fontSize: '0.8125rem', color: '#cbd5e1' }}>
{JSON.stringify(verifiedClaim, null, 2)}
          </pre>
          <div style={{ background: '#064e3b', padding: '12px', borderRadius: '6px', marginTop: '16px', color: '#a7f3d0', fontSize: '0.8125rem' }}>
            ✅ Citation Gate stripped 1 hallucinated URN! 100% citation resolution rate across 2 verified graph nodes.
          </div>
        </div>
      </div>
    </div>
  );
}
