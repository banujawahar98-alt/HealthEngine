import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  Heart,
  LayoutDashboard,
  ClipboardList,
  Smile,
  TrendingUp,
  Bot,
  BookOpen,
  UserCheck,
  ShieldAlert,
  LogOut,
  Menu,
  X,
  Settings
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import './Navbar.css';

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout, openCrisisModal } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="navbar-header">
      <div className="navbar-container">
        {/* Brand Logo */}
        <Link to="/" className="navbar-brand">
          <div className="logo-icon">
            <Heart size={22} color="#ffffff" fill="#ffffff" />
          </div>
          <div className="logo-text">
            <span className="brand-title">MindCare</span>
            <span className="brand-sub">Engine</span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className={`navbar-links ${mobileMenuOpen ? 'mobile-open' : ''}`}>
          {isAuthenticated ? (
            <>
              <Link
                to="/dashboard"
                className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </Link>
              <Link
                to="/assessments"
                className={`nav-link ${isActive('/assessments') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <ClipboardList size={18} />
                <span>Assessments</span>
              </Link>
              <Link
                to="/mood"
                className={`nav-link ${isActive('/mood') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <Smile size={18} />
                <span>Mood Tracker</span>
              </Link>
              <Link
                to="/progress"
                className={`nav-link ${isActive('/progress') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <TrendingUp size={18} />
                <span>Progress</span>
              </Link>
              <Link
                to="/ai"
                className={`nav-link ${isActive('/ai') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <Bot size={18} />
                <span>AI Support</span>
              </Link>
              <Link
                to="/resources"
                className={`nav-link ${isActive('/resources') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <BookOpen size={18} />
                <span>Resources</span>
              </Link>
              <Link
                to="/professionals"
                className={`nav-link ${isActive('/professionals') ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                <UserCheck size={18} />
                <span>Find Support</span>
              </Link>
              {user?.role === 'ADMIN' && (
                <Link
                  to="/admin"
                  className={`nav-link admin-link ${isActive('/admin') ? 'active' : ''}`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <Settings size={18} />
                  <span>Admin</span>
                </Link>
              )}
            </>
          ) : (
            <>
              <Link to="/resources" className="nav-link" onClick={() => setMobileMenuOpen(false)}>
                Resources
              </Link>
              <Link to="/professionals" className="nav-link" onClick={() => setMobileMenuOpen(false)}>
                Find Support
              </Link>
            </>
          )}
        </nav>

        {/* Right Actions */}
        <div className="navbar-actions">
          {/* Quick Crisis Helpline Trigger */}
          <button
            onClick={openCrisisModal}
            className="btn btn-outline-crisis btn-sm"
            title="Immediate Crisis Helplines"
          >
            <ShieldAlert size={16} />
            <span className="crisis-btn-text">Crisis Helpline</span>
          </button>

          {isAuthenticated && user ? (
            <div className="user-menu">
              <Link to="/profile" className="profile-link" title="Profile Settings">
                <div className="avatar">{user.name.charAt(0).toUpperCase()}</div>
                <div className="user-info">
                  <span className="user-name">{user.name}</span>
                  <span className="user-role-badge">{user.role}</span>
                </div>
              </Link>
              <button onClick={handleLogout} className="btn-logout" title="Sign Out">
                <LogOut size={18} />
              </button>
            </div>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="btn btn-secondary btn-sm">
                Log In
              </Link>
              <Link to="/register" className="btn btn-primary btn-sm">
                Get Started
              </Link>
            </div>
          )}

          {/* Mobile Menu Toggle */}
          <button className="mobile-toggle" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </div>
    </header>
  );
};
