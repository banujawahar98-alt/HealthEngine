import React from 'react';
import { Link } from 'react-router-dom';
import {
  ClipboardList,
  Smile,
  Bot,
  ShieldCheck,
  ArrowRight,
  ShieldAlert,
  Heart
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import './LandingPage.css';

export const LandingPage: React.FC = () => {
  const { isAuthenticated, openCrisisModal } = useAuth();

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="badge badge-primary mb-4">
            <Heart size={14} style={{ marginRight: 4 }} /> Empathetic & Evidence-Based
          </div>
          <h1 className="hero-title">
            AI-Powered Mental Health Assessment & Well-being Support Engine
          </h1>
          <p className="hero-subtitle">
            Understand your emotional well-being, track mood and stress trends, receive personalized safe support, and access evidence-based resources.
          </p>

          <div className="hero-actions">
            <Link to={isAuthenticated ? "/assessments" : "/register"} className="btn btn-primary btn-lg">
              Start Screening Assessment <ArrowRight size={20} />
            </Link>
            <Link to="/resources" className="btn btn-secondary btn-lg">
              Explore Resources
            </Link>
          </div>

          {/* Mandatory Disclaimer Box */}
          <div className="hero-disclaimer-box mt-4">
            <ShieldCheck size={20} color="#0d9488" style={{ flexShrink: 0 }} />
            <span>
              <strong>Platform Notice:</strong> This application provides screening and well-being support only. It does not diagnose mental-health conditions and does not replace professional medical care.
            </span>
          </div>
        </div>
      </section>

      {/* Feature Highlights Grid */}
      <section className="features-section">
        <div className="section-header text-center">
          <h2>Comprehensive Well-being Support System</h2>
          <p>Designed with standard questionnaires, safe AI guidance, and confidential tracking.</p>
        </div>

        <div className="grid-3">
          <div className="card feature-card">
            <div className="feature-icon" style={{ background: '#ccfbf1', color: '#0d9488' }}>
              <ClipboardList size={28} />
            </div>
            <h3>Validated Screening</h3>
            <p>
              Complete published screening instruments including PHQ-9 (Depression), GAD-7 (Anxiety), PSS-10 (Perceived Stress), and WHO-5 (Well-being).
            </p>
            <span className="feature-footer">Deterministic Python Scoring Service</span>
          </div>

          <div className="card feature-card">
            <div className="feature-icon" style={{ background: '#e0e7ff', color: '#4338ca' }}>
              <Bot size={28} />
            </div>
            <h3>MindCare AI & Safety Layer</h3>
            <p>
              Interact with a supportive assistant backed by RAG knowledge retrieval and automated safety monitoring for immediate distress detection.
            </p>
            <span className="feature-footer">Instant Crisis Protocol Guardrails</span>
          </div>

          <div className="card feature-card">
            <div className="feature-icon" style={{ background: '#fae8ff', color: '#86198f' }}>
              <Smile size={28} />
            </div>
            <h3>Mood & Stress Tracking</h3>
            <p>
              Record daily mood, stress, energy levels, and sleep hours. Visualize progress trends over time with dynamic interactive charts.
            </p>
            <span className="feature-footer">Personal Well-being Analytics</span>
          </div>
        </div>
      </section>

      {/* Standard Assessments Preview */}
      <section className="assessments-preview-section">
        <div className="section-header">
          <h2>Standardized Assessment Questionnaires</h2>
          <p>Select a validated instrument to start your screening.</p>
        </div>

        <div className="grid-2">
          <div className="card assessment-preview-card">
            <div className="flex-between">
              <span className="badge badge-primary">Depression Screening</span>
              <span className="time-estimate">9 Questions • ~3 mins</span>
            </div>
            <h3>PHQ-9 (Patient Health Questionnaire)</h3>
            <p>Monitors depressive symptom severity over the past 2 weeks using published scoring rules.</p>
            <Link to={isAuthenticated ? "/assessments/phq-9" : "/login"} className="btn btn-secondary btn-sm mt-4">
              Take PHQ-9 Screening &rarr;
            </Link>
          </div>

          <div className="card assessment-preview-card">
            <div className="flex-between">
              <span className="badge badge-primary">Anxiety Screening</span>
              <span className="time-estimate">7 Questions • ~2 mins</span>
            </div>
            <h3>GAD-7 (Generalized Anxiety Scale)</h3>
            <p>Assesses anxiety symptoms and nervousness over the preceding 14-day window.</p>
            <Link to={isAuthenticated ? "/assessments/gad-7" : "/login"} className="btn btn-secondary btn-sm mt-4">
              Take GAD-7 Screening &rarr;
            </Link>
          </div>
        </div>
      </section>

      {/* Urgent Crisis Helpline Banner */}
      <section className="crisis-callout-section">
        <div className="card crisis-callout-card">
          <div className="crisis-icon-wrap">
            <ShieldAlert size={36} color="#dc2626" />
          </div>
          <div className="crisis-text-wrap">
            <h3>Need Immediate Emergency Help?</h3>
            <p>
              If you or someone you know is in severe emotional distress or danger, please contact 24/7 crisis support immediately.
            </p>
          </div>
          <button onClick={openCrisisModal} className="btn btn-crisis btn-lg">
            Access 24/7 Helplines
          </button>
        </div>
      </section>
    </div>
  );
};
