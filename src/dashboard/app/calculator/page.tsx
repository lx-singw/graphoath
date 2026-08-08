'use client';

import React, { useState } from 'react';

export default function CalculatorPage() {
  const [actions, setActions] = useState(5000);
  const [hallucinationRate, setHallucinationRate] = useState(15.0);
  const [triageCost, setTriageCost] = useState(590.0);

  const hallucinatedWrites = Math.round(actions * (hallucinationRate / 100.0));
  const annualLossWithout = hallucinatedWrites * triageCost;
  const annualLossWith = 0;
  const netSavings = annualLossWithout - annualLossWith;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '1.75rem', margin: 0, fontWeight: 700 }}>Financial Cost of Hallucination ROI Calculator</h2>
        <p style={{ color: '#94a3b8', margin: '4px 0 0 0' }}>Calculate enterprise financial savings from gating AI agent write operations with GraphOath.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
        {/* Controls Panel */}
        <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px', padding: '24px' }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: '1.125rem', color: '#f8fafc' }}>Model Input Parameters</h3>
          
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.875rem', marginBottom: '8px' }}>
              Annual AI Agent Actions: <strong style={{ color: '#38bdf8' }}>{actions.toLocaleString()}</strong>
            </label>
            <input
              type="range"
              min="1000"
              max="50000"
              step="500"
              value={actions}
              onChange={(e) => setActions(Number(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.875rem', marginBottom: '8px' }}>
              LLM Hallucination Rate (%): <strong style={{ color: '#f59e0b' }}>{hallucinationRate.toFixed(1)}%</strong>
            </label>
            <input
              type="range"
              min="1.0"
              max="40.0"
              step="0.5"
              value={hallucinationRate}
              onChange={(e) => setHallucinationRate(Number(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', color: '#cbd5e1', fontSize: '0.875rem', marginBottom: '8px' }}>
              Triage Cost per Hallucinated Incident ($): <strong style={{ color: '#a855f7' }}>${triageCost.toFixed(2)}</strong>
            </label>
            <input
              type="range"
              min="100"
              max="2000"
              step="50"
              value={triageCost}
              onChange={(e) => setTriageCost(Number(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>
        </div>

        {/* Financial ROI Output Panel */}
        <div style={{ background: '#0f172a', border: '1px solid #10b981', borderRadius: '12px', padding: '24px' }}>
          <h3 style={{ margin: '0 0 20px 0', fontSize: '1.125rem', color: '#10b981' }}>Estimated Financial ROI Impact</h3>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Hallucinated Write Attempts:</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#fca5a5' }}>{hallucinatedWrites.toLocaleString()} attempts/yr</div>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Annual Incident Loss Without GraphOath:</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#ef4444' }}>${annualLossWithout.toLocaleString('en-US', { minimumFractionDigits: 2 })}</div>
          </div>

          <div style={{ borderTop: '1px solid #1e293b', paddingTop: '16px', marginTop: '16px' }}>
            <div style={{ color: '#64748b', fontSize: '0.875rem' }}>Net Annual ROI Savings With GraphOath:</div>
            <div style={{ fontSize: '2.25rem', fontWeight: 800, color: '#10b981', marginTop: '4px' }}>
              ${netSavings.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </div>
            <div style={{ color: '#a7f3d0', fontSize: '0.875rem', marginTop: '4px' }}>
              ✓ 100% ROI recovery by blocking hallucinated write operations at zero network overhead.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
