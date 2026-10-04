import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, CheckCircle2, ShieldCheck, AlertCircle } from 'lucide-react';
import { assessmentService } from '../../services/assessmentService';
import type { Assessment, Question } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const TakeAssessmentPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [responses, setResponses] = useState<Record<number, number>>({});
  const [ackConsent, setAckConsent] = useState(true);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDetail = async () => {
      if (!id) return;
      try {
        const res: any = await assessmentService.getAssessment(id);
        if (res.success) {
          setAssessment(res.data);
        }
      } catch (err: any) {
        setError(err.message || 'Failed to load assessment questions.');
      } finally {
        setLoading(false);
      }
    };
    fetchDetail();
  }, [id]);

  if (loading) return <LoadingSpinner message="Preparing screening questionnaire..." />;
  if (error || !assessment || !assessment.questions) {
    return (
      <div className="card text-center" style={{ maxWidth: 500, margin: '40px auto', padding: 32 }}>
        <AlertCircle size={40} color="#dc2626" style={{ margin: '0 auto 12px auto' }} />
        <h3>Unable to load questionnaire</h3>
        <p style={{ color: '#64748b' }}>{error || 'Questionnaire not found'}</p>
        <button onClick={() => navigate('/assessments')} className="btn btn-primary mt-4">
          Back to Assessments
        </button>
      </div>
    );
  }

  const questions: Question[] = assessment.questions;
  const currentQ = questions[currentIndex];
  const progressPercent = Math.round(((currentIndex + 1) / questions.length) * 100);

  const handleSelectOption = (qId: number, score: number) => {
    setResponses((prev) => ({ ...prev, [qId]: score }));
  };

  const isCurrentAnswered = responses[currentQ.questionId] !== undefined;
  const allAnswered = questions.every((q) => responses[q.questionId] !== undefined);

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setShowSubmitModal(true);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleSubmitFinal = async () => {
    if (!id || !allAnswered) return;
    setSubmitting(true);
    setError(null);
    try {
      const res: any = await assessmentService.submitAssessment(id, responses);
      if (res.success && res.data) {
        navigate(`/assessment-results/${res.data.id}`);
      }
    } catch (err: any) {
      setError(err.message || 'Submission failed. Please check your answers.');
      setShowSubmitModal(false);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: 720, margin: '20px auto 60px auto', display: 'flex', flexDirection: 'column', gap: 20 }}>
      {/* Top Header Card */}
      <div className="card" style={{ padding: 20 }}>
        <div className="flex-between mb-4">
          <button onClick={() => navigate('/assessments')} className="btn btn-secondary btn-sm">
            <ArrowLeft size={16} /> Exit
          </button>
          <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--primary-700)' }}>
            {assessment.name} Screening
          </span>
        </div>

        {/* Stepper Progress Bar */}
        <div style={{ marginBottom: 12 }}>
          <div className="flex-between" style={{ fontSize: '0.85rem', fontWeight: 600, color: '#64748b', marginBottom: 6 }}>
            <span>Question {currentIndex + 1} of {questions.length}</span>
            <span>{progressPercent}% Complete</span>
          </div>
          <div style={{ height: 8, background: '#e2e8f0', borderRadius: 999, overflow: 'hidden' }}>
            <div
              style={{
                height: '100%',
                width: `${progressPercent}%`,
                background: 'linear-gradient(90deg, #0d9488, #6366f1)',
                transition: 'width 0.3s ease'
              }}
            />
          </div>
        </div>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Main Question Card */}
      <div className="card" style={{ padding: 28 }}>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 24, lineHeight: 1.4 }}>
          {currentIndex + 1}. {currentQ.text}
        </h2>

        {/* Options Selection */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 28 }}>
          {currentQ.options.map((opt, idx) => {
            const isSelected = responses[currentQ.questionId] === opt.score;
            return (
              <div
                key={idx}
                onClick={() => handleSelectOption(currentQ.questionId, opt.score)}
                style={{
                  padding: '16px 20px',
                  borderRadius: 12,
                  border: isSelected ? '2px solid #0d9488' : '1px solid #e2e8f0',
                  backgroundColor: isSelected ? '#f0fdfa' : '#ffffff',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  transition: 'all 0.2s ease',
                  boxShadow: isSelected ? '0 2px 8px rgba(13, 148, 136, 0.15)' : 'none'
                }}
              >
                <span style={{ fontSize: '1rem', fontWeight: isSelected ? 700 : 500, color: isSelected ? '#0f766e' : '#334155' }}>
                  {opt.label}
                </span>
                {isSelected ? <CheckCircle2 size={20} color="#0d9488" /> : null}
              </div>
            );
          })}
        </div>

        {/* Navigation Buttons */}
        <div className="flex-between">
          <button
            onClick={handlePrev}
            disabled={currentIndex === 0}
            className="btn btn-secondary"
          >
            <ArrowLeft size={16} /> Previous
          </button>

          <button
            onClick={handleNext}
            disabled={!isCurrentAnswered}
            className="btn btn-primary"
          >
            <span>{currentIndex === questions.length - 1 ? 'Review & Submit' : 'Next Question'}</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </div>

      {/* Confirmation Modal */}
      {showSubmitModal && (
        <div className="modal-overlay" onClick={() => setShowSubmitModal(false)}>
          <div className="modal-container" onClick={(e) => e.stopPropagation()} style={{ maxWidth: 480 }}>
            <div className="text-center mb-4">
              <ShieldCheck size={44} color="#0d9488" style={{ margin: '0 auto 12px auto' }} />
              <h3 style={{ fontSize: '1.3rem', fontWeight: 800, color: 'var(--text-dark)' }}>Confirm Assessment Submission</h3>
              <p style={{ fontSize: '0.9rem', color: '#64748b' }}>
                You have answered all {questions.length} questions for {assessment.name}.
              </p>
            </div>

            <div style={{ background: '#f8fafc', padding: 14, borderRadius: 8, fontSize: '0.85rem', color: '#475569', marginBottom: 20 }}>
              <label style={{ display: 'flex', alignItems: 'flex-start', gap: 10, cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={ackConsent}
                  onChange={(e) => setAckConsent(e.target.checked)}
                  style={{ marginTop: 2 }}
                />
                <span>
                  I acknowledge that this screening provides educational feedback only and does not constitute a medical diagnosis.
                </span>
              </label>
            </div>

            <div style={{ display: 'flex', gap: 12 }}>
              <button
                onClick={() => setShowSubmitModal(false)}
                className="btn btn-secondary"
                style={{ flex: 1 }}
              >
                Back to Questions
              </button>
              <button
                onClick={handleSubmitFinal}
                disabled={!ackConsent || submitting}
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                {submitting ? 'Calculating Score...' : 'Submit & View Results'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
