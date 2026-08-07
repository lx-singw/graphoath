import React from 'react';

export const metadata = {
  title: 'GraphOath — Operator Dashboard',
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
        fontFamily: 'system-ui, -apple-system, sans-serif'
      }}>
        <header style={{
          borderBottom: '1px solid #1e293b',
          padding: '16px 32px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h1 style={{ margin: 0, fontSize: '1.25rem', color: '#38bdf8' }}>GraphOath</h1>
          <nav style={{ display: 'flex', gap: '16px' }}>
            <a href="/" style={{ color: '#94a3b8', textDecoration: 'none' }}>Overview</a>
            <a href="/ledger" style={{ color: '#94a3b8', textDecoration: 'none' }}>Ledger</a>
            <a href="/calculator" style={{ color: '#94a3b8', textDecoration: 'none' }}>ROI Calculator</a>
          </nav>

        </header>
        <main style={{ padding: '32px', maxWidth: '1200px', margin: '0 auto' }}>
          {children}
        </main>
      </body>
    </html>
  );
}
