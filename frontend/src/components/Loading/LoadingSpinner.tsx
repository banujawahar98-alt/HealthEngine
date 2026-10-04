import React from 'react';

export const LoadingSpinner: React.FC<{ message?: string }> = ({ message = "Loading MindCare..." }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '60px 20px', gap: 16 }}>
      <div style={{
        width: 44,
        height: 44,
        border: '4px solid #ccfbf1',
        borderTop: '4px solid #0d9488',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite'
      }} />
      <span style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-secondary)' }}>{message}</span>
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};
