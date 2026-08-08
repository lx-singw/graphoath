import React from 'react';

export const metadata = {
  title: 'GraphOath — Operator Governance Dashboard',
  description: 'The Evidence Engine for Agentic Data Governance',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{
        margin: 0,
        padding: 0,
        backgroundColor: '#020617',
        color: '#f8fafc',
        fontFamily: 'Inter, system-ui, -apple-system, sans-serif'
      }}>
        <header style={{
          borderBottom: '1px solid #1e293b',
          padding: '16px 32px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#0b0f19'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '1.5rem' }}>🛡️</span>
            <div>
              <h1 style={{ margin: 0, fontSize: '1.25rem', color: '#38bdf8', fontWeight: 700 }}>GraphOath</h1>
              <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Citation-Gated Control Plane for AI Agents</span>
            </div>
          </div>
          <nav style={{ display: 'flex', gap: '24px' }}>
            <a href="/" style={{ color: '#cbd5e1', textDecoration: 'none', fontWeight: 500 }}>Overview</a>
            <a href="/ledger" style={{ color: '#cbd5e1', textDecoration: 'none', fontWeight: 500 }}>Ledger Explorer</a>
            <a href="/approvals" style={{ color: '#cbd5e1', textDecoration: 'none', fontWeight: 500 }}>HITL Approvals</a>
            <a href="/diff" style={{ color: '#cbd5e1', textDecoration: 'none', fontWeight: 500 }}>Claim Diff Viewer</a>
            <a href="/calculator" style={{ color: '#cbd5e1', textDecoration: 'none', fontWeight: 500 }}>ROI Calculator</a>
          </nav>
        </header>
        <main style={{ padding: '32px', maxWidth: '1280px', margin: '0 auto' }}>
          {children}
        </main>
      </body>
    </html>
  );
}
