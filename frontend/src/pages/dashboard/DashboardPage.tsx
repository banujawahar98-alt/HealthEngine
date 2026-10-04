import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ClipboardList,
  Smile,
  Moon,
  Activity,
  Award,
  TrendingUp,
  Plus,
  Bot,
  AlertCircle
} from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  Legend
} from 'recharts';
import { dashboardService } from '../../services/dashboardService';
import type { DashboardSummary, DashboardTrends } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const DashboardPage: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [trends, setTrends] = useState<DashboardTrends | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [sumRes, trendRes]: [any, any] = await Promise.all([
          dashboardService.getSummary(),
          dashboardService.getTrends()
        ]);
        if (sumRes.success) setSummary(sumRes.data);
        if (trendRes.success) setTrends(trendRes.data);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard statistics.');
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  if (loading) return <LoadingSpinner message="Loading your well-being dashboard..." />;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Welcome Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #f0fdfa, #e0f2fe)', border: '1px solid #ccfbf1', padding: 28 }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f766e', marginBottom: 6 }}>
              Mental Well-being Dashboard
            </h1>
            <p style={{ color: '#334155', margin: 0, fontSize: '0.98rem' }}>
              Track your standardized screening scores, log daily mood, and visualize wellness trends over time.
            </p>
          </div>
          <div style={{ display: 'flex', gap: 12 }}>
            <Link to="/assessments" className="btn btn-primary">
              <ClipboardList size={18} /> New Assessment
            </Link>
            <Link to="/mood" className="btn btn-secondary">
              <Plus size={18} /> Log Mood
            </Link>
          </div>
        </div>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 14, borderRadius: 10, display: 'flex', alignItems: 'center', gap: 10 }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      {/* Summary Metrics Cards */}
      <div className="grid-4">
        {/* Card 1: Latest Assessment */}
        <div className="card" style={{ borderLeft: '4px solid #0d9488' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-secondary)' }}>LATEST ASSESSMENT</span>
            <ClipboardList size={20} color="#0d9488" />
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 4 }}>
            {summary?.latest_assessment.name || 'None Taken'}
          </h3>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
            <span style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0d9488' }}>
              {summary?.latest_assessment.score ?? '--'}
            </span>
            <span className="badge badge-primary">
              {summary?.latest_assessment.severity_level || 'No Data'}
            </span>
          </div>
        </div>

        {/* Card 2: Stress Level */}
        <div className="card" style={{ borderLeft: '4px solid #6366f1' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-secondary)' }}>STRESS LEVEL</span>
            <Activity size={20} color="#6366f1" />
          </div>
          <h3 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 4 }}>
            {summary?.latest_stress_level ? `${summary.latest_stress_level} / 5` : 'Not Recorded'}
          </h3>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            {summary?.latest_stress_level ? (summary.latest_stress_level > 3 ? 'Elevated Stress' : 'Moderate/Low Stress') : 'Log mood daily'}
          </span>
        </div>

        {/* Card 3: Current Mood */}
        <div className="card" style={{ borderLeft: '4px solid #8b5cf6' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-secondary)' }}>CURRENT MOOD</span>
            <Smile size={20} color="#8b5cf6" />
          </div>
          <h3 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 4 }}>
            {summary?.current_mood ? `${summary.current_mood} / 5` : 'Not Recorded'}
          </h3>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            1: Low &bull; 3: Neutral &bull; 5: Very Good
          </span>
        </div>

        {/* Card 4: Average Sleep */}
        <div className="card" style={{ borderLeft: '4px solid #059669' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-secondary)' }}>AVG SLEEP HOURS</span>
            <Moon size={20} color="#059669" />
          </div>
          <h3 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 4 }}>
            {summary?.average_sleep ? `${summary.average_sleep} hrs` : '--'}
          </h3>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            Target: 7 to 9 hours nightly
          </span>
        </div>
      </div>

      {/* Recharts Analytics Section */}
      <div className="grid-2">
        {/* Mood & Stress Trend Chart */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
            Daily Mood & Stress Trends
          </h3>
          {trends?.mood_trends && trends.mood_trends.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={trends.mood_trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
                <YAxis domain={[1, 5]} stroke="#64748b" fontSize={12} />
                <Tooltip contentStyle={{ background: '#ffffff', borderRadius: 8, border: '1px solid #cbd5e1' }} />
                <Legend />
                <Line type="monotone" dataKey="mood" name="Mood (1-5)" stroke="#0d9488" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="stress_level" name="Stress Level (1-5)" stroke="#dc2626" strokeWidth={2} strokeDasharray="4 4" dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ padding: 40, textAlign: 'center', color: '#64748b', fontSize: '0.9rem' }}>
              No mood entries recorded yet. Log your first daily entry to view trends!
            </div>
          )}
        </div>

        {/* Assessment Score Progress Chart */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
            Screening Score Progress
          </h3>
          {trends?.assessment_trends && trends.assessment_trends.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={trends.assessment_trends}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip contentStyle={{ background: '#ffffff', borderRadius: 8, border: '1px solid #cbd5e1' }} />
                <Legend />
                <Bar dataKey="score" name="Screening Score" fill="#6366f1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ padding: 40, textAlign: 'center', color: '#64748b', fontSize: '0.9rem' }}>
              No screening assessment completed yet. Take an assessment to see your progress chart!
            </div>
          )}
        </div>
      </div>

      {/* Quick Action Shortcuts */}
      <div className="card" style={{ background: '#ffffff' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 16 }}>
          Recommended Support Actions
        </h3>
        <div className="grid-3">
          <Link to="/ai" style={{ textDecoration: 'none' }}>
            <div style={{ border: '1px solid #e2e8f0', padding: 18, borderRadius: 12, background: '#f8fafc', transition: 'all 0.2s' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: '#4338ca', fontWeight: 700, marginBottom: 6 }}>
                <Bot size={20} /> MindCare AI Assistant
              </div>
              <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Chat confidentially for evidence-based self-care guidance.</p>
            </div>
          </Link>

          <Link to="/resources" style={{ textDecoration: 'none' }}>
            <div style={{ border: '1px solid #e2e8f0', padding: 18, borderRadius: 12, background: '#f8fafc', transition: 'all 0.2s' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: '#0d9488', fontWeight: 700, marginBottom: 6 }}>
                <TrendingUp size={20} /> Well-being Library
              </div>
              <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Explore articles on sleep hygiene, stress reduction, and mindfulness.</p>
            </div>
          </Link>

          <Link to="/professionals" style={{ textDecoration: 'none' }}>
            <div style={{ border: '1px solid #e2e8f0', padding: 18, borderRadius: 12, background: '#f8fafc', transition: 'all 0.2s' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: '#059669', fontWeight: 700, marginBottom: 6 }}>
                <Award size={20} /> Professional Support
              </div>
              <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>Locate licensed counselors and specialized support professionals.</p>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};
