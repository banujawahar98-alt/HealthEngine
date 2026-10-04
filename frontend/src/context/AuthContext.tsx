import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { authService } from '../services/authService';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isCrisisModalOpen: boolean;
  openCrisisModal: () => void;
  closeCrisisModal: () => void;
  login: (email: string, password: string) => Promise<void>;
  register: (data: any) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('mindcare_token'));
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isCrisisModalOpen, setIsCrisisModalOpen] = useState<boolean>(false);

  const openCrisisModal = () => setIsCrisisModalOpen(true);
  const closeCrisisModal = () => setIsCrisisModalOpen(false);

  useEffect(() => {
    // Trigger seed on first load to ensure DB has data (safe - uses upsert)
    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
    fetch(`${backendUrl}/api/admin/seed`, { method: 'POST' }).catch(() => {});

    const initAuth = async () => {
      const storedToken = localStorage.getItem('mindcare_token');
      if (storedToken) {
        try {
          const res: any = await authService.getMe();
          if (res.success && res.data) {
            setUser(res.data);
          } else {
            localStorage.removeItem('mindcare_token');
            setToken(null);
          }
        } catch (err) {
          localStorage.removeItem('mindcare_token');
          setToken(null);
        }
      }
      setIsLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const res: any = await authService.login({ email, password });
      if (res.success && res.data) {
        const { access_token, user: userData } = res.data;
        localStorage.setItem('mindcare_token', access_token);
        setToken(access_token);
        setUser(userData);
      }
    } catch (err: any) {
      const msg = err?.message || err?.detail?.message || err?.detail || 'Login failed.';
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: any) => {
    setIsLoading(true);
    try {
      const res: any = await authService.register(data);
      if (res.success && res.data) {
        const { access_token, user: userData } = res.data;
        localStorage.setItem('mindcare_token', access_token);
        setToken(access_token);
        setUser(userData);
      }
    } catch (err: any) {
      const msg = err?.message || err?.detail?.message || err?.detail || 'Registration failed.';
      throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('mindcare_token');
    setToken(null);
    setUser(null);
  };

  const refreshUser = async () => {
    try {
      const res: any = await authService.getMe();
      if (res.success && res.data) {
        setUser(res.data);
      }
    } catch (e) {
      // ignore
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        isCrisisModalOpen,
        openCrisisModal,
        closeCrisisModal,
        login,
        register,
        logout,
        refreshUser
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
