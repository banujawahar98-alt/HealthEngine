import React, { useState } from 'react';
import { Download, Trash2 } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { authService } from '../../services/authService';

export const ProfilePage: React.FC = () => {
  const { user, refreshUser, logout } = useAuth();

  const [name, setName] = useState(user?.name || '');
  const [ageRange, setAgeRange] = useState(user?.age_range || '25-34');
  const [updatingProfile, setUpdatingProfile] = useState(false);
  const [profileMsg, setProfileMsg] = useState<string | null>(null);

  // Password Change
  const [currentPwd, setCurrentPwd] = useState('');
  const [newPwd, setNewPwd] = useState('');
  const [pwdMsg, setPwdMsg] = useState<string | null>(null);
  const [changingPwd, setChangingPwd] = useState(false);

  // Data Export
  const [exporting, setExporting] = useState(false);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setUpdatingProfile(true);
    setProfileMsg(null);
    try {
      await authService.updateProfile({ name, age_range: ageRange });
      await refreshUser();
      setProfileMsg('Profile updated successfully.');
    } catch (err: any) {
      setProfileMsg('Failed to update profile.');
    } finally {
      setUpdatingProfile(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setChangingPwd(true);
    setPwdMsg(null);
    try {
      await authService.changePassword({ current_password: currentPwd, new_password: newPwd });
      setPwdMsg('Password updated successfully.');
      setCurrentPwd('');
      setNewPwd('');
    } catch (err: any) {
      setPwdMsg(err.message || 'Incorrect current password.');
    } finally {
      setChangingPwd(false);
    }
  };

  const handleExportData = async () => {
    setExporting(true);
    try {
      const res: any = await authService.exportData();
      if (res.success) {
        const jsonStr = JSON.stringify(res.data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `MindCare_User_Data_Export_${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
      }
    } catch (err) {
      alert('Failed to export user data.');
    } finally {
      setExporting(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? All your screening history and mood logs will be permanently erased.')) {
      return;
    }
    try {
      await authService.deleteAccount();
      logout();
    } catch (err) {
      alert('Failed to delete account.');
    }
  };

  if (!user) return null;

  return (
    <div style={{ maxWidth: 760, margin: '20px auto 60px auto', display: 'flex', flexDirection: 'column', gap: 24 }}>
      <div className="card" style={{ background: '#f8fafc', padding: 24 }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 4 }}>
          Account Settings & Profile
        </h1>
        <p style={{ color: '#64748b', margin: 0, fontSize: '0.92rem' }}>
          Manage your account information, security credentials, and data privacy options.
        </p>
      </div>

      <div className="grid-2">
        {/* Profile Info Form */}
        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
            User Information
          </h2>

          {profileMsg && (
            <div style={{ background: '#f0fdfa', border: '1px solid #ccfbf1', color: '#0f766e', padding: 10, borderRadius: 8, fontSize: '0.85rem', marginBottom: 14 }}>
              {profileMsg}
            </div>
          )}

          <form onSubmit={handleUpdateProfile}>
            <div className="form-group">
              <label>Full Name</label>
              <input
                type="text"
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                className="form-control"
                value={user.email}
                disabled
                style={{ backgroundColor: '#f1f5f9', cursor: 'not-allowed' }}
              />
            </div>

            <div className="form-group">
              <label>Age Range</label>
              <select className="form-control" value={ageRange} onChange={(e) => setAgeRange(e.target.value)}>
                <option value="Under 18">Under 18</option>
                <option value="18-24">18 - 24</option>
                <option value="25-34">25 - 34</option>
                <option value="35-44">35 - 44</option>
                <option value="45-54">45 - 54</option>
                <option value="55+">55+</option>
              </select>
            </div>

            <div className="form-group">
              <label>Account Role</label>
              <input
                type="text"
                className="form-control"
                value={user.role}
                disabled
                style={{ backgroundColor: '#f1f5f9' }}
              />
            </div>

            <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={updatingProfile}>
              {updatingProfile ? 'Updating...' : 'Save Profile Changes'}
            </button>
          </form>
        </div>

        {/* Security & Password Change */}
        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 18 }}>
            Change Password
          </h2>

          {pwdMsg && (
            <div style={{ background: '#f8fafc', border: '1px solid #cbd5e1', padding: 10, borderRadius: 8, fontSize: '0.85rem', marginBottom: 14 }}>
              {pwdMsg}
            </div>
          )}

          <form onSubmit={handleChangePassword}>
            <div className="form-group">
              <label>Current Password</label>
              <input
                type="password"
                className="form-control"
                placeholder="••••••••"
                value={currentPwd}
                onChange={(e) => setCurrentPwd(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>New Password</label>
              <input
                type="password"
                className="form-control"
                placeholder="At least 6 characters"
                value={newPwd}
                onChange={(e) => setNewPwd(e.target.value)}
                minLength={6}
                required
              />
            </div>

            <button type="submit" className="btn btn-secondary" style={{ width: '100%', marginTop: 8 }} disabled={changingPwd}>
              {changingPwd ? 'Updating Password...' : 'Update Password'}
            </button>
          </form>
        </div>
      </div>

      {/* Data Export & Account Deletion Card */}
      <div className="card">
        <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 16 }}>
          Data Privacy & Account Controls
        </h2>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <strong style={{ color: 'var(--text-dark)' }}>Export Personal Data</strong>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>
              Download a complete JSON export of your profile, screening assessment history, and mood logs.
            </p>
          </div>
          <button onClick={handleExportData} disabled={exporting} className="btn btn-secondary">
            <Download size={16} /> {exporting ? 'Exporting...' : 'Export JSON Data'}
          </button>
        </div>

        <div style={{ borderTop: '1px solid #e2e8f0', marginTop: 20, paddingTop: 20, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <strong style={{ color: '#dc2626' }}>Delete Account</strong>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: 0 }}>
              Permanently delete your account credentials, screening results, and mood logs.
            </p>
          </div>
          <button onClick={handleDeleteAccount} className="btn btn-crisis">
            <Trash2 size={16} /> Delete Account
          </button>
        </div>
      </div>
    </div>
  );
};
