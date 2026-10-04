import React, { useEffect, useState } from 'react';
import { TrendingUp, AlertCircle, ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';
import { assessmentService } from '../../services/assessmentService';
import type { AssessmentResult } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const ProgressPage: React.FC = () => {
  const [history, setHistory] = useState<AssessmentResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res: any = await assessmentService.getHistory();
        if (res.success) {
          setHistory(res.data);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load progress history.');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <LoadingSpinner message="Analyzing screening progress..." />;

  const latest = history.length > 0 ? history[0] : null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Header Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #e0e7ff, #f0fdfa)', border: '1px solid #c7d2fe', padding: 24 }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#3730a3', marginBottom: 6 }}>
          Screening Progress Tracking
        </h1>
        <p style={{ color: '#334155', margin: 0, fontSize: '0.95rem' }}>
          Compare previous and current screening scores using objective neutral wording to understand your long-term wellness trajectory.
        </p>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Latest Comparison Hero Box */}
      {latest ? (
        <div className="card" style={{ background: '#ffffff', padding: 28 }}>
          <div className="flex-between mb-4">
            <span className="badge badge-primary">{latest.assessment_name} LATEST COMPARISON</span>
            <span style={{ fontSize: '0.85rem', color: '#64748b' }}>Date: {latest.created_at.slice(0, 10)}</span>
          </div>

          <div className="grid-3" style={{ margin: '20px 0' }}>
            <div style={{ background: '#f8fafc', padding: 20, borderRadius: 12, textAlign: 'center', border: '1px solid #e2e8f0' }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748b' }}>PREVIOUS SCORE</span>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#475569', marginTop: 4 }}>
                {latest.previous_score !== null && latest.previous_score !== undefined ? latest.previous_score : 'N/A'}
              </div>
            </div>

            <div style={{ background: '#f0fdfa', padding: 20, borderRadius: 12, textAlign: 'center', border: '1px solid #ccfbf1' }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#0d9488' }}>CURRENT SCORE</span>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#0d9488', marginTop: 4 }}>
                {latest.score} <span style={{ fontSize: '1rem', color: '#94a3b8' }}>/ {latest.max_score}</span>
              </div>
            </div>

            <div style={{ background: '#f8fafc', padding: 20, borderRadius: 12, textAlign: 'center', border: '1px solid #e2e8f0' }}>
              <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#64748b' }}>TREND STATUS</span>
              <div style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-dark)', marginTop: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
                {latest.previous_score !== null && latest.previous_score !== undefined ? (
                  latest.score < latest.previous_score ? (
                    <><ArrowDownRight color="#059669" size={24} /> Decreased</>
                  ) : latest.score > latest.previous_score ? (
                    <><ArrowUpRight color="#dc2626" size={24} /> Increased</>
                  ) : (
                    <><Minus color="#64748b" size={24} /> Unchanged</>
                  )
                ) : (
                  <span>First Screening</span>
                )}
              </div>
            </div>
          </div>

          <div style={{ background: '#f1f5f9', padding: 14, borderRadius: 8, fontSize: '0.92rem', color: '#334155' }}>
            <strong>Observation Summary:</strong><br />
            {latest.trend_summary || "This is your initial screening attempt for this questionnaire. Future submissions will display comparative trend analysis."}
          </div>
        </div>
      ) : (
        <div className="card text-center" style={{ padding: 40 }}>
          <TrendingUp size={40} color="#94a3b8" style={{ margin: '0 auto 12px auto' }} />
          <h3>No Assessment Data Available</h3>
          <p style={{ color: '#64748b' }}>Complete a screening questionnaire to view comparative progress analysis.</p>
        </div>
      )}

      {/* History Timeline Table */}
      <div className="card">
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
          Complete Screening History ({history.length})
        </h2>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left' }}>
                <th style={{ padding: '12px 16px' }}>Date</th>
                <th style={{ padding: '12px 16px' }}>Assessment</th>
                <th style={{ padding: '12px 16px' }}>Score</th>
                <th style={{ padding: '12px 16px' }}>Severity Level</th>
                <th style={{ padding: '12px 16px' }}>Trend Wording</th>
              </tr>
            </thead>
            <tbody>
              {history.map((r) => (
                <tr key={r.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '12px 16px', fontWeight: 600 }}>{r.created_at.slice(0, 10)}</td>
                  <td style={{ padding: '12px 16px' }}>{r.assessment_name}</td>
                  <td style={{ padding: '12px 16px', fontWeight: 700, color: '#0d9488' }}>
                    {r.score} / {r.max_score}
                  </td>
                  <td style={{ padding: '12px 16px' }}>
                    <span className="badge badge-primary">{r.severity_level}</span>
                  </td>
                  <td style={{ padding: '12px 16px', color: '#64748b', fontSize: '0.85rem' }}>
                    {r.trend_summary || 'Baseline screening'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
