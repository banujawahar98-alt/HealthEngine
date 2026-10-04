import React from 'react';
import { X, Phone, ExternalLink, ShieldAlert } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const CrisisModal: React.FC = () => {
  const { isCrisisModalOpen, closeCrisisModal } = useAuth();

  if (!isCrisisModalOpen) return null;

  return (
    <div className="modal-overlay" onClick={closeCrisisModal}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()} style={{ borderTop: '6px solid var(--crisis-red)' }}>
        <button
          onClick={closeCrisisModal}
          style={{ position: 'absolute', top: 16, right: 16, border: 'none', background: 'transparent', cursor: 'pointer' }}
        >
          <X size={20} color="#64748b" />
        </button>

        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
          <div style={{ background: 'var(--crisis-bg)', padding: 10, borderRadius: '50%', color: 'var(--crisis-red)' }}>
            <ShieldAlert size={28} />
          </div>
          <div>
            <h3 style={{ fontSize: '1.25rem', color: '#991b1b', margin: 0 }}>Immediate Safety & Crisis Support</h3>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Free, confidential support available 24/7</p>
          </div>
        </div>

        <p style={{ fontSize: '0.95rem', color: '#334155', marginBottom: 20 }}>
          If you or someone you know is experiencing a life-threatening emergency, suicidal crisis, or severe emotional distress, please reach out to immediate emergency services right away:
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 24 }}>
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 10, padding: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <strong style={{ color: '#991b1b' }}>988 Suicide & Crisis Lifeline</strong>
                <p style={{ fontSize: '0.85rem', color: '#7f1d1d', margin: 0 }}>Call or text 988 (US & Canada)</p>
              </div>
              <a href="tel:988" className="btn btn-sm btn-crisis" style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                <Phone size={14} /> Call 988
              </a>
            </div>
          </div>

          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, padding: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <strong style={{ color: '#1e293b' }}>Crisis Text Line</strong>
                <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Text HOME to 741741</p>
              </div>
              <a href="sms:741741?body=HOME" className="btn btn-sm btn-secondary" style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                Text 741741
              </a>
            </div>
          </div>

          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, padding: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <strong style={{ color: '#1e293b' }}>Kiran Mental Health Helpline (India)</strong>
                <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Toll-Free 1800-599-0019</p>
              </div>
              <a href="tel:18005990019" className="btn btn-sm btn-secondary" style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
                <Phone size={14} /> Call Helpline
              </a>
            </div>
          </div>

          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, padding: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <strong style={{ color: '#1e293b' }}>International Crisis Directory (IASP)</strong>
                <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Find emergency helplines in your country</p>
              </div>
              <a
                href="https://www.iasp.info/resources/Crisis_Centres"
                target="_blank"
                rel="noreferrer"
                className="btn btn-sm btn-secondary"
                style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}
              >
                Visit IASP <ExternalLink size={14} />
              </a>
            </div>
          </div>
        </div>

        <div style={{ background: '#f1f5f9', borderRadius: 8, padding: 12, fontSize: '0.85rem', color: '#475569', textAlign: 'center' }}>
          MindCare provides well-being screening and education only. It does not replace medical or emergency evaluation.
        </div>
      </div>
    </div>
  );
};
