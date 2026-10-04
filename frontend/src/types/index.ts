export interface User {
  id: string;
  name: string;
  email: string;
  role: 'USER' | 'PROFESSIONAL' | 'ADMIN';
  age_range?: string;
  created_at: string;
  updated_at?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface AssessmentOption {
  label: string;
  score: number;
}

export interface Question {
  questionId: number;
  text: string;
  order: number;
  options: AssessmentOption[];
}

export interface Assessment {
  id: string;
  name: string;
  description: string;
  version: string;
  type: string;
  active: boolean;
  question_count: number;
  questions?: Question[];
}

export interface AssessmentResult {
  id: string;
  user_id: string;
  assessment_id: string;
  assessment_name: string;
  score: number;
  max_score: number;
  severity_level: string;
  interpretation: string;
  disclaimer: string;
  suggested_next_steps: string[];
  previous_score?: number;
  trend_summary?: string;
  created_at: string;
}

export interface MoodEntry {
  id: string;
  user_id: string;
  mood: number; // 1-5
  stress_level: number; // 1-5
  energy_level: number; // 1-5
  sleep_hours: number;
  note?: string;
  created_at: string;
}

export interface DashboardSummary {
  latest_assessment: {
    name: string;
    score: number;
    severity_level: string;
    date?: string;
  };
  latest_stress_level: number;
  current_mood: number;
  average_sleep: number;
  assessments_completed: number;
}

export interface TrendItem {
  date: string;
  mood?: number;
  stress_level?: number;
  energy_level?: number;
  sleep_hours?: number;
  assessment_name?: string;
  score?: number;
  max_score?: number;
  severity_level?: string;
}

export interface DashboardTrends {
  mood_trends: TrendItem[];
  assessment_trends: TrendItem[];
}

export interface CrisisHelpline {
  id: string;
  name: string;
  description: string;
  phone: string;
  website?: string;
  country: string;
  availability: string;
  source?: string;
  active: boolean;
}

export interface SafetyAnalysis {
  risk_level: 'NORMAL' | 'DISTRESS' | 'HIGH_RISK' | 'IMMEDIATE_SAFETY_CONCERN';
  is_crisis: boolean;
  safety_message?: string;
  crisis_helplines?: CrisisHelpline[];
}

export interface ChatMessage {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  message: string;
  created_at: string;
  safety_analysis?: SafetyAnalysis;
}

export interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

export interface ResourceItem {
  id: string;
  title: string;
  description: string;
  content: string;
  category: string;
  tags: string[];
  source?: string;
  url?: string;
  created_at: string;
}

export interface ProfessionalItem {
  id: string;
  name: string;
  qualification: string;
  specialization: string;
  experience: string;
  location: string;
  consultation_mode: string;
  availability: string;
  contact_email?: string;
  contact_phone?: string;
  bio?: string;
  is_mock: boolean;
  created_at: string;
}

export interface AdminAnalytics {
  summary_cards: {
    total_users: number;
    total_assessments_completed: number;
    active_resources: number;
    verified_professionals: number;
  };
  anonymized_analytics: {
    severity_distribution: { severity: string; count: number }[];
    assessment_type_distribution: { type: string; count: number }[];
  };
}
