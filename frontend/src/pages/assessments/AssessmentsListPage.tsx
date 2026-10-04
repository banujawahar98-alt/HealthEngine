import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, AlertCircle } from 'lucide-react';
import { assessmentService } from '../../services/assessmentService';
import type { Assessment } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const AssessmentsListPage: React.FC = () => {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res: any = await assessmentService.getAssessments();
        if (res.success) {
          setAssessments(res.data);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load assessments');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <LoadingSpinner message="Loading mental health questionnaires..." />;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      <div className="card" style={{ background: '#f0fdfa', border: '1px solid #ccfbf1', padding: 24 }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f766e', marginBottom: 6 }}>
          Standardized Mental Health Screening Questionnaires
        </h1>
        <p style={{ color: '#334155', margin: 0, fontSize: '0.95rem' }}>
          Select a validated screening tool below. Answers are processed deterministically using official published scoring algorithms.
        </p>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      <div className="grid-2">
        {assessments.map((a) => (
          <div key={a.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: 16 }}>
            <div>
              <div className="flex-between" style={{ marginBottom: 10 }}>
                <span className="badge badge-primary">{a.type.toUpperCase()}</span>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#64748b' }}>
                  {a.question_count} Questions
                </span>
              </div>
              <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 8 }}>
                {a.name}
              </h2>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {a.description}
              </p>
            </div>

            <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: 14, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.78rem', color: '#94a3b8', fontWeight: 600 }}>Version {a.version}</span>
              <Link to={`/assessments/${a.id}`} className="btn btn-primary btn-sm">
                Start Assessment <ArrowRight size={16} />
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
