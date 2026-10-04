import React, { useEffect, useState } from 'react';
import { Trash2, Calendar, AlertCircle } from 'lucide-react';
import { moodService } from '../../services/moodService';
import type { MoodEntry } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const MoodTrackerPage: React.FC = () => {
  const [entries, setEntries] = useState<MoodEntry[]>([]);
  const [loading, setLoading] = useState(true);

  // Form State
  const [mood, setMood] = useState<number>(4);
  const [stress, setStress] = useState<number>(3);
  const [energy, setEnergy] = useState<number>(3);
  const [sleep, setSleep] = useState<number>(7.5);
  const [note, setNote] = useState<string>('');
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEntries = async () => {
    try {
      const res: any = await moodService.getMoodEntries();
      if (res.success) {
        setEntries(res.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load mood entries.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEntries();
  }, []);

  const handleAddSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      const res: any = await moodService.addMoodEntry({
        mood,
        stress_level: stress,
        energy_level: energy,
        sleep_hours: Number(sleep),
        note
      });
      if (res.success) {
        setNote('');
        fetchEntries();
      }
    } catch (err: any) {
      setError(err.message || 'Failed to save mood entry.');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this mood log?')) return;
    try {
      await moodService.deleteMoodEntry(id);
      fetchEntries();
    } catch (err: any) {
      alert('Failed to delete mood log.');
    }
  };

  if (loading) return <LoadingSpinner message="Loading mood tracker..." />;

  const moodLabels = ['1 - Very Low', '2 - Low', '3 - Neutral', '4 - Good', '5 - Very Good'];
  const stressLabels = ['1 - Very Low', '2 - Low', '3 - Moderate', '4 - High', '5 - Very High'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Header Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #fae8ff, #f0fdfa)', border: '1px solid #f5d0fe', padding: 24 }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#701a75', marginBottom: 6 }}>
          Daily Mood & Stress Tracker
        </h1>
        <p style={{ color: '#334155', margin: 0, fontSize: '0.95rem' }}>
          Record your daily emotional state, stress levels, energy, and sleep duration to track long-term well-being trends.
        </p>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8, display: 'flex', alignItems: 'center', gap: 8 }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Main Grid: Entry Form & History */}
      <div className="grid-2">
        {/* Form Card */}
        <div className="card">
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 20 }}>
            Log Today's Entry
          </h2>

          <form onSubmit={handleAddSubmit}>
            {/* Mood Slider/Select */}
            <div className="form-group">
              <label>Mood Level: {moodLabels[mood - 1]}</label>
              <input
                type="range"
                min="1"
                max="5"
                value={mood}
                onChange={(e) => setMood(Number(e.target.value))}
                style={{ width: '100%', accentColor: '#0d9488' }}
              />
              <div className="flex-between" style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <span>Very Low</span>
                <span>Neutral</span>
                <span>Very Good</span>
              </div>
            </div>

            {/* Stress Level */}
            <div className="form-group">
              <label>Stress Level: {stressLabels[stress - 1]}</label>
              <input
                type="range"
                min="1"
                max="5"
                value={stress}
                onChange={(e) => setStress(Number(e.target.value))}
                style={{ width: '100%', accentColor: '#dc2626' }}
              />
              <div className="flex-between" style={{ fontSize: '0.75rem', color: '#64748b' }}>
                <span>Very Low</span>
                <span>Moderate</span>
                <span>Very High</span>
              </div>
            </div>

            {/* Energy Level */}
            <div className="form-group">
              <label>Energy Level (1 to 5)</label>
              <select className="form-control" value={energy} onChange={(e) => setEnergy(Number(e.target.value))}>
                <option value={1}>1 - Low Energy / Exhausted</option>
                <option value={2}>2 - Below Average</option>
                <option value={3}>3 - Moderate Energy</option>
                <option value={4}>4 - High Energy</option>
                <option value={5}>5 - Excellent / Energetic</option>
              </select>
            </div>

            {/* Sleep Hours */}
            <div className="form-group">
              <label>Sleep Hours Last Night</label>
              <input
                type="number"
                step="0.5"
                min="0"
                max="24"
                className="form-control"
                value={sleep}
                onChange={(e) => setSleep(Number(e.target.value))}
                required
              />
            </div>

            {/* Optional Note */}
            <div className="form-group">
              <label>Daily Note (Optional)</label>
              <textarea
                className="form-control"
                placeholder="What affected your mood or stress today? (e.g., exams, workout, restful sleep)..."
                value={note}
                onChange={(e) => setNote(e.target.value)}
                maxLength={500}
              />
            </div>

            <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={saving}>
              {saving ? 'Saving Log...' : 'Save Mood Log'}
            </button>
          </form>
        </div>

        {/* History List */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-dark)', marginBottom: 20 }}>
            Recent Mood History ({entries.length})
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 14, overflowY: 'auto', maxHeight: 520 }}>
            {entries.length === 0 ? (
              <div style={{ textAlign: 'center', padding: 40, color: '#64748b', fontSize: '0.9rem' }}>
                No mood entries recorded yet. Fill out the form to log your first day!
              </div>
            ) : (
              entries.map((item) => (
                <div key={item.id} style={{ border: '1px solid #e2e8f0', padding: 16, borderRadius: 12, background: '#f8fafc' }}>
                  <div className="flex-between mb-4">
                    <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#475569', display: 'flex', alignItems: 'center', gap: 6 }}>
                      <Calendar size={14} /> {item.created_at.slice(0, 10)}
                    </span>
                    <button onClick={() => handleDelete(item.id)} className="btn-logout" title="Delete log">
                      <Trash2 size={16} color="#dc2626" />
                    </button>
                  </div>

                  <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 10 }}>
                    <span className="badge badge-primary">Mood: {item.mood}/5</span>
                    <span className="badge badge-warning">Stress: {item.stress_level}/5</span>
                    <span className="badge badge-success">Sleep: {item.sleep_hours} hrs</span>
                  </div>

                  {item.note && (
                    <p style={{ fontSize: '0.88rem', color: '#334155', margin: 0, fontStyle: 'italic', background: '#ffffff', padding: 8, borderRadius: 6, border: '1px solid #cbd5e1' }}>
                      "{item.note}"
                    </p>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
