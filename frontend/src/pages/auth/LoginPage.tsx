import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, Lock, Mail, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid email or password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: '60px auto 100px auto', padding: 20 }}>
      <div className="card" style={{ padding: 32 }}>
        <div className="text-center mb-4">
          <div className="logo-icon" style={{ margin: '0 auto 12px auto' }}>
            <Heart size={22} color="#ffffff" fill="#ffffff" />
          </div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-dark)' }}>Sign in to MindCare</h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Welcome back! Access your well-being dashboard</p>
        </div>

        {error && (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8, fontSize: '0.85rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email Address</label>
            <div style={{ position: 'relative' }}>
              <input
                type="email"
                className="form-control"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{ paddingLeft: 38 }}
              />
              <Mail size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
            </div>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                className="form-control"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={{ paddingLeft: 38 }}
              />
              <Lock size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-lg mt-4" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div style={{ marginTop: 24, padding: 16, background: '#f8fafc', borderRadius: 8, border: '1px dashed #cbd5e1' }}>
          <span style={{ fontSize: '0.82rem', fontWeight: 700, color: '#475569', display: 'block', marginBottom: 8 }}>
            Quick Demo Login Buttons:
          </span>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={() => {
                setEmail('user@mindcare.org');
                setPassword('UserPass123!');
              }}
              className="btn btn-secondary btn-sm"
              style={{ flex: 1, fontSize: '0.8rem', padding: '6px 10px' }}
            >
              Fill Demo User
            </button>
            <button
              type="button"
              onClick={() => {
                setEmail('admin@mindcare.org');
                setPassword('AdminPass123!');
              }}
              className="btn btn-secondary btn-sm"
              style={{ flex: 1, fontSize: '0.8rem', padding: '6px 10px' }}
            >
              Fill Demo Admin
            </button>
          </div>
        </div>

        <div className="text-center mt-4" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          Don't have an account? <Link to="/register" style={{ fontWeight: 600 }}>Create an account</Link>
        </div>
      </div>
    </div>
  );
};
