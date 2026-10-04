import React, { useEffect, useState } from 'react';
import { BookOpen, Search, ExternalLink, X } from 'lucide-react';
import { resourceService } from '../../services/resourceService';
import type { ResourceItem } from '../../types';
import { LoadingSpinner } from '../../components/Loading/LoadingSpinner';

export const ResourcesPage: React.FC = () => {
  const [resources, setResources] = useState<ResourceItem[]>([]);
  const [category, setCategory] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedResource, setSelectedResource] = useState<ResourceItem | null>(null);
  const [error, setError] = useState<string | null>(null);

  const categories = [
    'All',
    'Stress',
    'Anxiety',
    'Sleep',
    'Academic Pressure',
    'Work Pressure',
    'Mindfulness',
    'Relaxation',
    'Emotional Well-being',
    'Professional Support'
  ];

  const fetchResources = async (catOverride?: string, searchOverride?: string) => {
    setLoading(true);
    try {
      const targetCat = catOverride !== undefined ? catOverride : category;
      const targetSearch = searchOverride !== undefined ? searchOverride : search;
      const catParam = targetCat === 'All' ? '' : targetCat;
      const res: any = await resourceService.getResources(catParam, undefined, targetSearch);
      if (res.success) {
        setResources(res.data);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load resource library.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResources();
  }, [category]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Reset category filter to 'All' when searching so results span all categories
    setCategory('');
    fetchResources('', search);
  };

  const handleResetFilters = () => {
    setSearch('');
    setCategory('');
    fetchResources('', '');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 28 }}>
      {/* Header Banner */}
      <div className="card" style={{ background: 'linear-gradient(135deg, #f0fdfa, #e0f2fe)', border: '1px solid #ccfbf1', padding: 24 }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f766e', marginBottom: 6 }}>
          Mental Health Resource Library
        </h1>
        <p style={{ color: '#334155', margin: 0, fontSize: '0.95rem' }}>
          Explore curated evidence-informed guides, sleep hygiene recommendations, mindfulness practices, and academic stress management strategies.
        </p>
      </div>

      {error && (
        <div style={{ background: '#fef2f2', border: '1px solid #fecaca', color: '#991b1b', padding: 12, borderRadius: 8 }}>
          {error}
        </div>
      )}

      {/* Search & Category Filter Controls */}
      <div className="card" style={{ padding: 20 }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
          <div style={{ position: 'relative', flex: 1 }}>
            <input
              type="text"
              className="form-control"
              placeholder="Search articles by title, topic, or keyword..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ paddingLeft: 38 }}
            />
            <Search size={18} color="#94a3b8" style={{ position: 'absolute', left: 12, top: 12 }} />
          </div>
          <button type="submit" className="btn btn-primary">
            Search
          </button>
        </form>

        {/* Category Chips */}
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          {categories.map((cat) => {
            const isSelected = (cat === 'All' && !category) || category === cat;
            return (
              <button
                key={cat}
                onClick={() => setCategory(cat === 'All' ? '' : cat)}
                style={{
                  padding: '6px 14px',
                  borderRadius: 9999,
                  border: isSelected ? '1px solid #0d9488' : '1px solid #e2e8f0',
                  backgroundColor: isSelected ? '#0d9488' : '#ffffff',
                  color: isSelected ? '#ffffff' : '#475569',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
              >
                {cat}
              </button>
            );
          })}
        </div>
      </div>

      {loading ? (
        <LoadingSpinner message="Searching well-being resources..." />
      ) : resources.length === 0 ? (
        <div className="card text-center" style={{ padding: 40 }}>
          <BookOpen size={36} color="#94a3b8" style={{ margin: '0 auto 12px auto' }} />
          <h3>No Resources Found</h3>
          <p style={{ color: '#64748b', marginBottom: 16 }}>
            {category && search
              ? `No articles found matching "${search}" in "${category}".`
              : category
              ? `No articles found under "${category}".`
              : `No articles found matching "${search}".`}
          </p>
          <button onClick={handleResetFilters} className="btn btn-secondary btn-sm">
            Show All Resources
          </button>
        </div>
      ) : (
        /* Resource Cards Grid */
        <div className="grid-3">
          {resources.map((item) => (
            <div
              key={item.id}
              className="card"
              onClick={() => setSelectedResource(item)}
              style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', cursor: 'pointer' }}
            >
              <div>
                <span className="badge badge-primary mb-4">{item.category}</span>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 8 }}>
                  {item.title}
                </h3>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: 14 }}>
                  {item.description}
                </p>
              </div>

              <div>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12 }}>
                  {item.tags.map((t, idx) => (
                    <span key={idx} style={{ fontSize: '0.72rem', background: '#f1f5f9', color: '#64748b', padding: '2px 8px', borderRadius: 4 }}>
                      #{t}
                    </span>
                  ))}
                </div>
                <div style={{ fontSize: '0.8rem', color: '#0d9488', fontWeight: 700, display: 'flex', alignItems: 'center', gap: 4 }}>
                  Read Guide &rarr;
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal Reader for Selected Resource */}
      {selectedResource && (
        <div className="modal-overlay" onClick={() => setSelectedResource(null)}>
          <div className="modal-container" onClick={(e) => e.stopPropagation()} style={{ maxWidth: 680 }}>
            <button
              onClick={() => setSelectedResource(null)}
              style={{ position: 'absolute', top: 16, right: 16, border: 'none', background: 'transparent', cursor: 'pointer' }}
            >
              <X size={20} color="#64748b" />
            </button>

            <span className="badge badge-primary mb-4">{selectedResource.category}</span>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--text-dark)', marginBottom: 12 }}>
              {selectedResource.title}
            </h2>

            {selectedResource.source && (
              <div style={{ fontSize: '0.82rem', color: '#64748b', marginBottom: 16 }}>
                Source: <strong>{selectedResource.source}</strong>
              </div>
            )}

            <div style={{ borderTop: '1px solid #e2e8f0', paddingTop: 16, fontSize: '0.96rem', color: '#334155', lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>
              {selectedResource.content}
            </div>

            {selectedResource.url && (
              <div style={{ marginTop: 24, paddingTop: 16, borderTop: '1px solid #e2e8f0' }}>
                <a href={selectedResource.url} target="_blank" rel="noreferrer" className="btn btn-secondary btn-sm" style={{ display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                  Visit External Reference <ExternalLink size={14} />
                </a>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
