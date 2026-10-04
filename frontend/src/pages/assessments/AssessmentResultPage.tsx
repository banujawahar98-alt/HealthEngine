import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Download,
  CheckCircle,
  AlertTriangle,
  ArrowLeft,
  AlertCircle
} from 'lucide-react';
import { assessmentService } from '../../services/assessmentService';
import type { AssessmentResult } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const AssessmentResultPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const fetchResult = async () => {
      if (!id) return;
      try {
        const res: any = await assessmentService.getResult(id);
        if (res.success) {
          setResult(res.data);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load assessment result');
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [id]);

  const handleDownloadPdf = async () => {
    if (!result || !id) return;
    setDownloading(true);
    try {
      const filename = `MindCare_Screening_${result.assessment_name}_${result.created_at.slice(0, 10)}.pdf`;
      await assessmentService.downloadPdf(id, filename);
    } catch (err) {
      alert('Failed to generate PDF report. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return <LoadingSpinner message="Generating assessment report..." />;

  if (error || !result) {
    return (
      <div className="card text-center" style={{ maxWidth: 500, margin: '40px auto', padding: 32 }}>
        <AlertCircle size={40} color="#dc2626" style={{ margin: '0 auto 12px auto' }} />
        <h3>Result Not Found</h3>
        <p style={{ color: '#64748b' }}>{error || 'Unable to retrieve screening result.'}</p>
        <Link to="/dashboard" className="btn btn-primary mt-4">
          Return to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 760, margin: '20px auto 60px auto', display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Top Header Card */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #f0fdfa, #f1f5f9)', border: '1px solid #ccfbf1', padding: 28 }}>
        <div className="flex-between mb-4">
          <span className="badge badge-primary">SCREENING REPORT</span>
          <span style={{ fontSize: '0.85rem', color: '#64748b', fontWeight: 600 }}>
            {result.created_at.slice(0, 10)}
          </span>
        </div>

        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 6 }}>
          {result.assessment_name} Assessment Result
        </h1>
        <p style={{ color: '#475569', margin: 0, fontSize: '0.95rem' }}>
          Official scoring evaluation completed deterministically.
        </p>

        {/* Big Score Gauge Box */}
        <div style={{ marginTop: 24, padding: 20, background: '#ffffff', borderRadius: 14, border: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-around', flexWrap: 'wrap', gap: 16 }}>
          <div style={{ textAlign: 'center' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>YOUR SCORE</span>
            <div style={{ fontSize: '2.5rem', fontWeight: 900, color: '#0d9488', lineHeight: 1 }}>
              {result.score} <span style={{ fontSize: '1.2rem', color: '#94a3b8', fontWeight: 600 }}>/ {result.max_score}</span>
            </div>
          </div>

          <div style={{ height: 40, width: 1, background: '#e2e8f0' }} />

          <div style={{ textAlign: 'center' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748b', textTransform: 'uppercase' }}>SEVERITY LEVEL</span>
            <div style={{ marginTop: 4 }}>
              <span className="badge badge-primary" style={{ fontSize: '0.9rem', padding: '6px 14px' }}>
                {result.severity_level}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Mandatory Disclaimer Box */}
      <div style={{ background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: 12, padding: 16, color: '#1e40af', fontSize: '0.88rem', display: 'flex', alignItems: 'center', gap: 12 }}>
        <AlertTriangle size={20} color="#1d4ed8" style={{ flexShrink: 0 }} />
        <span>
          <strong>Important Notice:</strong> This screening result is not a diagnosis. It provides educational insight to help monitor well-being over time.
        </span>
      </div>

      {/* What this means */}
      <div className="card">
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 12 }}>
          What This Score Means
        </h3>
        <p style={{ fontSize: '0.98rem', color: '#334155', lineHeight: 1.6, marginBottom: 16 }}>
          {result.interpretation}
        </p>

        {result.trend_summary && (
          <div style={{ background: '#f8fafc', borderLeft: '4px solid #6366f1', padding: 14, borderRadius: 8, fontSize: '0.9rem', color: '#475569' }}>
            <strong>Comparison with previous screening:</strong><br />
            {result.trend_summary}
          </div>
        )}
      </div>

      {/* Suggested Next Steps */}
      <div className="card">
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 16 }}>
          Suggested Next Steps
        </h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          {result.suggested_next_steps.map((step, idx) => (
            <div key={idx} style={{ display: 'flex', alignItems: 'flex-start', gap: 12, background: '#f8fafc', padding: 14, borderRadius: 10 }}>
              <CheckCircle size={18} color="#0d9488" style={{ marginTop: 2, flexShrink: 0 }} />
              <span style={{ fontSize: '0.94rem', color: '#334155' }}>{step}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Action Toolbar */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap' }}>
        <Link to="/dashboard" className="btn btn-secondary">
          <ArrowLeft size={16} /> Back to Dashboard
        </Link>

        <div style={{ display: 'flex', gap: 12 }}>
          <Link to="/progress" className="btn btn-secondary">
            View Progress Trends
          </Link>

          <button
            onClick={handleDownloadPdf}
            disabled={downloading}
            className="btn btn-primary"
          >
            <Download size={18} /> {downloading ? 'Downloading PDF...' : 'Download PDF Report'}
          </button>
        </div>
      </div>
    </div>
  );
};
