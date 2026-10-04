import React, { useEffect, useState } from 'react';
import { MapPin, Clock, Mail, Phone, Search, Award } from 'lucide-react';
import { professionalService } from '../../services/professionalService';
import type { ProfessionalItem } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const ProfessionalsPage: React.FC = () => {
  const [professionals, setProfessionals] = useState<ProfessionalItem[]>([]);
  const [specialization, setSpecialization] = useState<string>('');
  const [mode, setMode] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfessionals = async () => {
    setLoading(true);
    setError(null);
    try {
      const res: any = await professionalService.getProfessionals(specialization, undefined, mode, search);
      if (res.success) {
        setProfessionals(res.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load professional support directory.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfessionals();
  }, [specialization, mode]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchProfessionals();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Header Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #f0fdfa, #f1f5f9)', border: '1px solid #ccfbf1', padding: 24 }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f766e', marginBottom: 6 }}>
          Find Professional Support
        </h1>
        <p style={{ color: '#334155', margin: 0, fontSize: '0.95rem' }}>
          Locate qualified licensed psychologists, counselors, and mental-health specialists for online or in-person consultation.
        </p>

        {/* Academic Mock Data Notice */}
        <div style={{ marginTop: 14, background: '#fffbeb', border: '1px solid #fde68a', color: '#b45309', padding: '8px 12px', borderRadius: 6, fontSize: '0.82rem' }}>
          <strong>Notice:</strong> The directory below contains clearly labeled sample demonstration profiles for academic project illustration.
        </div>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8 }}>
          {error}
        </div>
      )}

      {/* Filter Controls */}
      <div className="card" style={{ padding: 20 }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr auto', gap: 12 }}>
          <div style={{ position: 'relative' }}>
            <input
              type="text"
              className="form-control"
              placeholder="Search by practitioner name or qualification..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: 38 }}
            />
            <Search size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
          </div>

          <select className="form-control" value={specialization} onChange={(e) => setSpecialization(e.target.value)}>
            <option value="">All Specializations</option>
            <option value="Anxiety">Anxiety & Stress</option>
            <option value="Depression">Mood & Depression</option>
            <option value="Academic">Academic & Student Stress</option>
            <option value="Psychiatry">Psychiatry</option>
          </select>

          <select className="form-control" value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="">All Modes</option>
            <option value="Online">Online Consultation</option>
            <option value="In-Person">In-Person</option>
          </select>

          <button type="submit" className="btn btn-primary">
            Filter
          </button>
        </form>
      </div>

      {loading ? (
        <LoadingSpinner message="Searching professional directory..." />
      ) : (
        <div className="grid-2">
          {professionals.map((p) => (
            <div key={p.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: 16 }}>
              <div>
                <div className="flex-between mb-4">
                  <span className="badge badge-primary">{p.consultation_mode}</span>
                  {p.is_mock && <span className="badge badge-warning">Demonstration Profile</span>}
                </div>

                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 4 }}>
                  {p.name}
                </h2>
                <div style={{ fontSize: '0.88rem', fontWeight: 600, color: '#0d9488', marginBottom: 12 }}>
                  {p.qualification} &bull; {p.experience} Exp.
                </div>

                <p style={{ fontSize: '0.9rem', color: '#475569', marginBottom: 14 }}>
                  {p.bio}
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: '0.85rem', color: '#64748b' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <Award size={16} color="#6366f1" /> Specialization: <strong>{p.specialization}</strong>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <MapPin size={16} color="#059669" /> Location: <strong>{p.location}</strong>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <Clock size={16} color="#d97706" /> Availability: <strong>{p.availability}</strong>
                  </div>
                </div>
              </div>

              <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: 14, display: 'flex', gap: 10 }}>
                {p.contact_phone && (
                  <a href={`tel:${p.contact_phone}`} className="btn btn-secondary btn-sm" style={{ flex: 1 }}>
                    <Phone size={14} /> {p.contact_phone}
                  </a>
                )}
                {p.contact_email && (
                  <a href={`mailto:${p.contact_email}`} className="btn btn-primary btn-sm" style={{ flex: 1 }}>
                    <Mail size={14} /> Email Consultation
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
