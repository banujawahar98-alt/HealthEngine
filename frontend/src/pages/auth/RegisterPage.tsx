import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Heart, User as UserIcon, Mail, Lock, AlertCircle } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const RegisterPage: React.FC = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [ageRange, setAgeRange] = useState('25-34');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await register({
        name,
        email,
        password,
        confirm_password: confirmPassword,
        age_range: ageRange,
        role: 'USER'
      });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Registration failed. Please check details.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 480, margin: '50px auto 100px auto', padding: 20 }}>
      <div className="card" style={{ padding: 32 }}>
        <div className="text-center mb-4">
          <div className="logo-icon" style={{ margin: '0 auto 12px auto' }}>
            <Heart size={22} color="#ffffff" fill="#ffffff" />
          </div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-dark)' }}>Create Your MindCare Account</h2>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Private, secure mental-health screening & well-being support</p>
        </div>

        {error && (
          <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8, fontSize: '0.85rem', marginBottom: 16, display: 'flex', alignItems: 'center', gap: 8 }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                className="form-control"
                placeholder="Jane Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                style={{ paddingLeft: 38 }}
              />
              <UserIcon size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
            </div>
          </div>

          <div className="form-group">
            <label>Email Address</label>
            <div style={{ position: 'relative' }}>
              <input
                type="email"
                className="form-control"
                placeholder="jane@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                style={{ paddingLeft: 38 }}
              />
              <Mail size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
            </div>
          </div>

          <div className="form-group">
            <label>Age Range (Optional)</label>
            <select
              className="form-control"
              value={ageRange}
              onChange={(e) => setAgeRange(e.target.value)}
            >
              <option value="Under 18">Under 18</option>
              <option value="18-24">18 - 24</option>
              <option value="25-34">25 - 34</option>
              <option value="35-44">35 - 44</option>
              <option value="45-54">45 - 54</option>
              <option value="55+">55+</option>
            </select>
          </div>

          <div className="form-group">
            <label>Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                className="form-control"
                placeholder="At least 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                minLength={6}
                required
                style={{ paddingLeft: 38 }}
              />
              <Lock size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
            </div>
          </div>

          <div className="form-group">
            <label>Confirm Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type="password"
                className="form-control"
                placeholder="Re-enter password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                minLength={6}
                required
                style={{ paddingLeft: 38 }}
              />
              <Lock size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-lg mt-4" style={{ width: '100%' }} disabled={loading}>
            {loading ? 'Creating Account...' : 'Register & Start'}
          </button>
        </form>

        <div className="text-center mt-4" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          Already have an account? <Link to="/login" style={{ fontWeight: 600 }}>Sign in</Link>
        </div>
      </div>
    </div>
  );
};
