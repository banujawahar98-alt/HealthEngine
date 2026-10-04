import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, ShieldAlert } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import './Footer.css';

export const Footer: React.FC = () => {
  const { openCrisisModal } = useAuth();

  return (
    <footer className="app-footer">
      <div className="footer-container">
        <div className="footer-grid">
          {/* Brand Info */}
          <div className="footer-brand">
            <div className="footer-logo">
              <Heart size={20} color="#0d9488" fill="#0d9488" />
              <span>MindCare Support Engine</span>
            </div>
            <p className="footer-desc">
              An AI-powered mental health screening, self-assessment tracking, and well-being support platform.
            </p>
            <div className="legal-notice">
              <p>
                <strong>Important Notice:</strong> This application provides screening and well-being support only. It does not diagnose mental-health conditions and does not replace professional medical care.
              </p>
            </div>
          </div>

          {/* Quick Links */}
          <div className="footer-links-col">
            <h4 className="footer-col-title">Navigation</h4>
            <ul>
              <li><Link to="/assessments">Mental Health Screening</Link></li>
              <li><Link to="/mood">Daily Mood Tracker</Link></li>
              <li><Link to="/progress">Progress Dashboard</Link></li>
              <li><Link to="/ai">MindCare AI Assistant</Link></li>
              <li><Link to="/resources">Well-being Library</Link></li>
              <li><Link to="/professionals">Professional Directory</Link></li>
            </ul>
          </div>

          {/* Emergency Crisis Helplines */}
          <div className="footer-crisis-col">
            <h4 className="footer-col-title" style={{ color: 'var(--crisis-red)' }}>
              <ShieldAlert size={16} /> Emergency Crisis Contacts
            </h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: 12 }}>
              If you are in immediate danger or emotional crisis, reach out 24/7:
            </p>
            <ul className="crisis-list">
              <li>
                <strong>988 Suicide & Crisis Lifeline:</strong> Call/Text <a href="tel:988">988</a>
              </li>
              <li>
                <strong>Crisis Text Line:</strong> Text <code>HOME</code> to <a href="sms:741741">741741</a>
              </li>
              <li>
                <strong>Kiran Helpline (India):</strong> <a href="tel:18005990019">1800-599-0019</a>
              </li>
            </ul>
            <button onClick={openCrisisModal} className="btn btn-outline-crisis btn-sm mt-4" style={{ width: '100%' }}>
              View All Crisis Helplines
            </button>
          </div>
        </div>

        <div className="footer-bottom">
          <span>&copy; {new Date().getFullYear()} MindCare Engine. Academic & Screening Support System.</span>
          <div className="footer-legal-links">
            <a href="#disclaimer" onClick={(e) => { e.preventDefault(); alert("Medical Disclaimer:\n\nThis platform is strictly an informational screening tool. Scores generated (PHQ-9, GAD-7, PSS, WHO-5) are for personal tracking and screening insight only and do not constitute clinical diagnoses."); }}>Disclaimer</a>
            <span>•</span>
            <a href="#privacy" onClick={(e) => { e.preventDefault(); alert("Privacy Notice:\n\nUser assessment data, mood logs, and AI conversations are stored securely with user authorization. Personal data is never shared with third parties."); }}>Privacy Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
};
