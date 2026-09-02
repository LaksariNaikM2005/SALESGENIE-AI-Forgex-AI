import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Sparkles, Award, ArrowUpRight, CheckCircle, Lightbulb, Filter, RefreshCw, Zap, Search, ChevronRight, Cpu } from 'lucide-react';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  const fetchRecommendations = () => {
    setLoading(true);
    const query = priorityFilter !== 'all' ? `?priority=${priorityFilter}` : '';
    api.get(`/recommendations${query}`)
      .then(res => setRecommendations(res.data.recommendations || []))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchRecommendations();
  }, [priorityFilter]);

  const handleGenerateAll = async () => {
    setGenerating(true);
    try {
      const res = await api.post('/recommendations/generate-all');
      alert(res.data?.message || 'Generated AI recommendations for all prospects!');
      fetchRecommendations();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to generate recommendations');
    } finally {
      setGenerating(false);
    }
  };

  const handleToggleComplete = async (id, currentStatus) => {
    try {
      await api.put(`/recommendations/${id}`, { completed: !currentStatus });
      fetchRecommendations();
    } catch (err) {
      alert('Failed to update recommendation status');
    }
  };

  const filteredRecommendations = recommendations.filter(item => {
    const matchesSearch = !search ||
      item.recommendation?.toLowerCase().includes(search.toLowerCase()) ||
      item.lead_company?.toLowerCase().includes(search.toLowerCase()) ||
      item.lead_contact?.toLowerCase().includes(search.toLowerCase()) ||
      item.reason?.toLowerCase().includes(search.toLowerCase());

    return matchesSearch;
  });

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <div>
          <h2 className="fw-bold text-light mb-1 d-flex align-items-center gap-2">
            <Sparkles className="text-warning" size={28} /> AI Next-Best-Action Recommendations
          </h2>
          <p className="text-muted mb-0">Real-time intelligent recommendations linked directly to manufacturing prospects & ML scores</p>
        </div>
        <div className="d-flex align-items-center gap-2">
          <button className="btn btn-warning d-flex align-items-center gap-2 fw-semibold" onClick={handleGenerateAll} disabled={generating}>
            <Zap size={16} className={generating ? 'spin' : ''} /> {generating ? 'Generating Insights...' : 'Generate AI Insights for All Prospects'}
          </button>
          <button className="btn btn-outline-light d-flex align-items-center gap-2" onClick={fetchRecommendations}>
            <RefreshCw size={16} /> Refresh
          </button>
        </div>
      </div>

      {/* Filter Toolbar in Recommendations */}
      <div className="card border-secondary p-3 mb-4" style={{ backgroundColor: '#1e293b' }}>
        <div className="row g-3 align-items-center">
          <div className="col-md-5">
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-muted"><Search size={16} /></span>
              <input
                type="text"
                className="form-control bg-dark text-light border-secondary"
                placeholder="Search recommendations, companies, or contacts..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
          <div className="col-md-4">
            <div className="d-flex align-items-center gap-2">
              <span className="small text-muted me-1"><Filter size={14} /> Priority:</span>
              {['all', 'High', 'Medium', 'Low'].map((p) => (
                <button
                  key={p}
                  className={`btn btn-sm ${priorityFilter === p ? 'btn-primary' : 'btn-outline-secondary text-light'}`}
                  onClick={() => setPriorityFilter(p)}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
          <div className="col-md-3 text-md-end text-muted small">
            <span>Connected Recommendations: <strong className="text-light">{filteredRecommendations.length}</strong></span>
          </div>
        </div>
      </div>

      {/* Recommendations Cards */}
      <div className="row g-4">
        {loading ? (
          <div className="col-12 text-center py-5"><div className="spinner-border text-primary"></div></div>
        ) : filteredRecommendations.length === 0 ? (
          <div className="col-12 text-center py-5 card border-secondary text-muted" style={{ backgroundColor: '#1e293b' }}>
            <Lightbulb size={48} className="mx-auto mb-2 opacity-50 text-warning" />
            <p>No AI recommendations match your filter. Click "Generate AI Insights for All Prospects" to refresh!</p>
          </div>
        ) : (
          filteredRecommendations.map((item) => (
            <div key={item.id} className="col-md-6">
              <div className={`card border-secondary h-100 p-4 ${item.completed ? 'opacity-75' : ''}`} style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
                <div className="d-flex align-items-center justify-content-between mb-3">
                  <div className="d-flex align-items-center gap-2">
                    <span className={`badge ${item.priority === 'High' ? 'bg-danger' : item.priority === 'Medium' ? 'bg-warning text-dark' : 'bg-info'} px-2 py-1`}>
                      {item.priority} Priority
                    </span>
                    {item.sector && (
                      <span className="badge bg-dark border border-secondary text-info px-2 py-1">
                        {item.sector}
                      </span>
                    )}
                  </div>
                  {item.lead_score && (
                    <span className="badge bg-success-subtle text-success border border-success px-2 py-1">
                      {item.lead_score} ML Score
                    </span>
                  )}
                </div>

                <h5 className="fw-bold text-white mb-2">{item.recommendation}</h5>
                <p className="small text-muted mb-3" style={{ color: '#cbd5e1' }}><strong>Rationale:</strong> {item.reason}</p>

                {/* Connected Prospect Link Section */}
                <div className="mt-auto pt-3 border-top border-secondary d-flex align-items-center justify-content-between">
                  <Link to={`/leads/${item.lead_id}`} className="btn btn-sm btn-outline-info d-flex align-items-center gap-1">
                    Connected Prospect: <strong>{item.lead_company}</strong> <ChevronRight size={14} />
                  </Link>
                  <button
                    onClick={() => handleToggleComplete(item.id, item.completed)}
                    className={`btn btn-sm ${item.completed ? 'btn-success' : 'btn-outline-primary'} d-flex align-items-center gap-1`}
                  >
                    <CheckCircle size={16} /> {item.completed ? 'Completed' : 'Mark Completed'}
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Recommendations;
