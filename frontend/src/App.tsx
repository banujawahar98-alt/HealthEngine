import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar/Navbar';
import { Footer } from './components/Footer/Footer';
import { CrisisModal } from './components/Modal/CrisisModal';

import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { AssessmentsListPage } from './pages/assessments/AssessmentsListPage';
import { TakeAssessmentPage } from './pages/assessments/TakeAssessmentPage';
import { AssessmentResultPage } from './pages/assessments/AssessmentResultPage';
import { MoodTrackerPage } from './pages/mood/MoodTrackerPage';
import { ProgressPage } from './pages/progress/ProgressPage';
import { AiAssistantPage } from './pages/ai/AiAssistantPage';
import { ResourcesPage } from './pages/resources/ResourcesPage';
import { ProfessionalsPage } from './pages/professionals/ProfessionalsPage';
import { ProfilePage } from './pages/profile/ProfilePage';
import { AdminDashboardPage } from './pages/admin/AdminDashboardPage';

// Protected Route Wrapper for Authenticated Users
const ProtectedRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  if (isLoading) return null;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
};

// Admin Route Wrapper
const AdminRoute: React.FC<{ children: React.ReactElement }> = ({ children }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  if (isLoading) return null;
  if (!isAuthenticated || user?.role !== 'ADMIN') return <Navigate to="/dashboard" replace />;
  return children;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', background: 'var(--bg-gradient)' }}>
          <Navbar />
          <main style={{ flex: 1, padding: '24px 16px', maxWidth: 1200, width: '100%', margin: '0 auto', boxSizing: 'border-box' }}>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/resources" element={<ResourcesPage />} />
              <Route path="/professionals" element={<ProfessionalsPage />} />

              {/* Protected User Routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/assessments"
                element={
                  <ProtectedRoute>
                    <AssessmentsListPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/assessments/:id"
                element={
                  <ProtectedRoute>
                    <TakeAssessmentPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/assessment-results/:id"
                element={
                  <ProtectedRoute>
                    <AssessmentResultPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/mood"
                element={
                  <ProtectedRoute>
                    <MoodTrackerPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/progress"
                element={
                  <ProtectedRoute>
                    <ProgressPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/ai"
                element={
                  <ProtectedRoute>
                    <AiAssistantPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                }
              />

              {/* Protected Admin Routes */}
              <Route
                path="/admin"
                element={
                  <AdminRoute>
                    <AdminDashboardPage />
                  </AdminRoute>
                }
              />

              {/* Fallback Catch-All */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <Footer />
          <CrisisModal />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
