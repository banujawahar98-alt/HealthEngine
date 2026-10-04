import React, { useEffect, useState } from 'react';
import {
  Users,
  ClipboardList,
  BookOpen,
  UserCheck,
  Plus,
  AlertCircle
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { adminService } from '../../services/adminService';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

const COLORS = ['#0d9488', '#6366f1', '#f59e0b', '#dc2626', '#8b5cf6'];

export const AdminDashboardPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // New Resource Form Modal
  const [showResourceModal, setShowResourceModal] = useState(false);
  const [resTitle, setResTitle] = useState('');
  const [resDesc, setResDesc] = useState('');
  const [resCat, setResCat] = useState('Stress');
  const [resContent, setResContent] = useState('');
  const [savingRes, setSavingRes] = useState(false);

  const fetchAnalytics = async () => {
    try {
      const res: any = await adminService.getAnalytics();
      if (res.success) {
        setAnalytics(res.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load admin analytics. Admin privileges required.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const handleCreateResource = async (e: React.FormEvent) => {
    e.preventDefault();
    setSavingRes(true);
    try {
      await adminService.createResource({
        title: resTitle,
        description: resDesc,
        category: resCat,
        content: resContent,
        tags: [resCat.toLowerCase(), 'general']
      });
      setShowResourceModal(false);
      setResTitle('');
      setResDesc('');
      setResContent('');
      fetchAnalytics();
    } catch (err: any) {
      alert('Failed to create resource.');
    } finally {
      setSavingRes(false);
    }
  };

  if (loading) return <LoadingSpinner message="Loading anonymized admin analytics..." />;

  if (error) {
    return (
      <div className="card text-center" style={{ maxWidth: 500, margin: '40px auto', padding: 32 }}>
        <AlertCircle size={40} color="#dc2626" style={{ margin: '0 auto 12px auto' }} />
        <h3>Access Restricted</h3>
        <p style={{ color: '#64748b' }}>{error}</p>
      </div>
    );
  }

  const cards = analytics?.summary_cards || {};
  const severityDist = analytics?.anonymized_analytics?.severity_distribution || [];
  const typeDist = analytics?.anonymized_analytics?.assessment_type_distribution || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Header Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #1e293b, #0f172a)', color: '#ffffff', padding: 28 }}>
        <div className="flex-between">
          <div>
            <span className="badge" style={{ background: '#3b82f6', color: '#ffffff', marginBottom: 8 }}>
              ADMINISTRATIVE PORTAL
            </span>
            <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#ffffff', marginBottom: 6 }}>
              Aggregated Analytics & Platform Management
            </h1>
            <p style={{ color: '#94a3b8', margin: 0, fontSize: '0.95rem' }}>
              Monitor system utilization, anonymized screening concern distributions, and manage well-being resources.
            </p>
          </div>

          <button onClick={() => setShowResourceModal(true)} className="btn btn-primary">
            <Plus size={18} /> Add New Resource
          </button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid-4">
        <div className="card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="flex-between mb-4">
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b' }}>REGISTERED USERS</span>
            <Users size={20} color="#3b82f6" />
          </div>
          <h3 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-dark)' }}>
            {cards.total_users ?? 0}
          </h3>
        </div>

        <div className="card" style={{ borderLeft: '4px solid #0d9488' }}>
          <div className="flex-between mb-4">
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b' }}>ASSESSMENTS TAKEN</span>
            <ClipboardList size={20} color="#0d9488" />
          </div>
          <h3 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-dark)' }}>
            {cards.total_assessments_completed ?? 0}
          </h3>
        </div>

        <div className="card" style={{ borderLeft: '4px solid #8b5cf6' }}>
          <div className="flex-between mb-4">
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b' }}>ACTIVE RESOURCES</span>
            <BookOpen size={20} color="#8b5cf6" />
          </div>
          <h3 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-dark)' }}>
            {cards.active_resources ?? 0}
          </h3>
        </div>

        <div className="card" style={{ borderLeft: '4px solid #059669' }}>
          <div className="flex-between mb-4">
            <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#64748b' }}>PROFESSIONALS</span>
            <UserCheck size={20} color="#059669" />
          </div>
          <h3 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-dark)' }}>
            {cards.verified_professionals ?? 0}
          </h3>
        </div>
      </div>

      {/* Analytics Charts */}
      <div className="grid-2">
        {/* Severity Distribution */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
            Anonymized Symptom Severity Distribution
          </h3>
          {severityDist.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={severityDist}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="severity" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip contentStyle={{ background: '#ffffff', borderRadius: 8 }} />
                <Bar dataKey="count" fill="#0d9488" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ textAlign: 'center', padding: 40, color: '#64748b' }}>No screening data logged yet</div>
          )}
        </div>

        {/* Assessment Type Breakdown */}
        <div className="card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
            Screening Instrument Usage
          </h3>
          {typeDist.length > 0 ? (
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={typeDist}
                  dataKey="count"
                  nameKey="type"
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  label={(entry: any) => `${entry.type}: ${entry.count}`}
                >
                  {typeDist.map((_: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div style={{ textAlign: 'center', padding: 40, color: '#64748b' }}>No assessment data logged yet</div>
          )}
        </div>
      </div>

      {/* Modal for Creating Resource */}
      {showResourceModal && (
        <div className="modal-overlay" onClick={() => setShowResourceModal(false)}>
          <div className="modal-container" onClick={(e) => e.stopPropagation()} style={{ maxWidth: 540 }}>
            <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 16 }}>
              Add Knowledge Library Resource
            </h3>

            <form onSubmit={handleCreateResource}>
              <div className="form-group">
                <label>Article Title</label>
                <input
                  type="text"
                  className="form-control"
                  value={resTitle}
                  onChange={(e) => setResTitle(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Category</label>
                <select className="form-control" value={resCat} onChange={(e) => setResCat(e.target.value)}>
                  <option value="Stress">Stress</option>
                  <option value="Anxiety">Anxiety</option>
                  <option value="Sleep">Sleep</option>
                  <option value="Academic Pressure">Academic Pressure</option>
                  <option value="Mindfulness">Mindfulness</option>
                  <option value="Relaxation">Relaxation</option>
                </select>
              </div>

              <div className="form-group">
                <label>Short Description</label>
                <input
                  type="text"
                  className="form-control"
                  value={resDesc}
                  onChange={(e) => setResDesc(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label>Full Content</label>
                <textarea
                  className="form-control"
                  rows={4}
                  value={resContent}
                  onChange={(e) => setResContent(e.target.value)}
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: 12, marginTop: 20 }}>
                <button type="button" onClick={() => setShowResourceModal(false)} className="btn btn-secondary" style={{ flex: 1 }}>
                  Cancel
                </button>
                <button type="submit" disabled={savingRes} className="btn btn-primary" style={{ flex: 1 }}>
                  {savingRes ? 'Creating...' : 'Save Resource'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
