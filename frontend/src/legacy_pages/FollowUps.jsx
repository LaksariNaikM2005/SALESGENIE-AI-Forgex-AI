import React, { useState, useEffect } from 'react';
import api from '../services/api';
import {
  Calendar, Clock, CheckCircle2, Plus, Sparkles, Trash2, Check,
  Target, AlertTriangle, TrendingUp, Brain, DollarSign, ChevronDown, ChevronUp
} from 'lucide-react';

const FollowUps = () => {
  const [followups, setFollowups] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [expandedAI, setExpandedAI] = useState({});

  const [newFollowup, setNewFollowup] = useState({
    lead_id: '',
    notes: '',
    follow_up_at: new Date(Date.now() + 86400000 * 2).toISOString().slice(0, 16),
    status: 'pending',
  });

  const [leads, setLeads] = useState([]);

  const fetchFollowups = () => {
    setLoading(true);
    const query = filter !== 'all' ? `?status=${filter}` : '';
    api.get(`/followups${query}`)
      .then(res => setFollowups(res.data.followups || []))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchFollowups();
    api.get('/leads?per_page=200&page=1')
      .then(res => setLeads(res.data.leads || res.data || []))
      .catch(() => {});
  }, [filter]);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newFollowup.lead_id) {
      alert('Please select a prospect lead');
      return;
    }
    try {
      await api.post(`/leads/${newFollowup.lead_id}/followups`, {
        notes: newFollowup.notes,
        follow_up_at: newFollowup.follow_up_at,
        status: newFollowup.status,
      });
      setShowModal(false);
      setNewFollowup({ ...newFollowup, notes: '', lead_id: '' });
      fetchFollowups();
    } catch (err) {
      alert(err.response?.data?.message || 'Failed to schedule follow-up');
    }
  };

  const handleStatusUpdate = async (id, status) => {
    try {
      await api.put(`/followups/${id}`, { status });
      fetchFollowups();
    } catch (err) {
      alert('Failed to update status');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this follow-up task?')) return;
    try {
      await api.delete(`/followups/${id}`);
      fetchFollowups();
    } catch (err) {
      alert('Failed to delete follow-up');
    }
  };

  const toggleAI = (id) => setExpandedAI(prev => ({ ...prev, [id]: !prev[id] }));

  const priorityColor = (p) => {
    if (!p) return 'bg-secondary';
    switch (p.toLowerCase()) {
      case 'high': return 'bg-danger';
      case 'medium': return 'bg-warning text-dark';
      case 'low': return 'bg-info text-dark';
      default: return 'bg-secondary';
    }
  };

  const riskIcon = (r) => {
    if (!r) return null;
    switch (r.toLowerCase()) {
      case 'low':    return <span className="text-success fw-semibold">✓ Low Risk</span>;
      case 'medium': return <span className="text-warning fw-semibold">⚠ Medium Risk</span>;
      case 'high':   return <span className="text-danger fw-semibold">✗ High Risk</span>;
      default: return null;
    }
  };

  return (
    <div>
      {/* Header */}
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1 d-flex align-items-center gap-2">
            <Calendar className="text-primary" size={28} /> Scheduled Follow-ups &amp; Reminders
          </h2>
          <p className="text-muted mb-0">
            Track upcoming buyer touchpoints, AI next-best-actions, and mark tasks completed
          </p>
        </div>
        <button className="btn btn-primary d-flex align-items-center gap-2" onClick={() => setShowModal(true)}>
          <Plus size={18} /> Schedule Follow-up
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="card border-secondary p-3 mb-4" style={{ backgroundColor: '#1e293b' }}>
        <div className="d-flex align-items-center justify-content-between">
          <div className="btn-group">
            {['all', 'pending', 'completed'].map((f) => (
              <button
                key={f}
                className={`btn btn-sm text-capitalize ${filter === f ? 'btn-primary' : 'btn-outline-secondary text-light'}`}
                onClick={() => setFilter(f)}
              >
                {f} Tasks
              </button>
            ))}
          </div>
          <span className="small text-muted">Total: {followups.length} Tasks</span>
        </div>
      </div>

      {/* Follow-ups List */}
      <div className="row g-3">
        {loading ? (
          <div className="col-12 text-center py-5"><div className="spinner-border text-primary" /></div>
        ) : followups.length === 0 ? (
          <div className="col-12 text-center py-5 card border-secondary text-muted" style={{ backgroundColor: '#1e293b' }}>
            <Clock size={48} className="mx-auto mb-2 opacity-50 text-secondary" />
            <p>No follow-ups found. Click "Schedule Follow-up" to add one!</p>
          </div>
        ) : (
          followups.map((item) => (
            <div key={item.id} className="col-md-6 col-lg-4">
              <div className="card border-secondary h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
                {/* Card Header */}
                <div className="card-header border-secondary d-flex align-items-center justify-content-between"
                     style={{ backgroundColor: '#0f172a' }}>
                  <span className={`badge text-capitalize px-2 py-1 ${item.status === 'completed' ? 'bg-success' : item.status === 'cancelled' ? 'bg-secondary' : 'bg-warning text-dark'}`}>
                    {item.status === 'completed'
                      ? <><CheckCircle2 size={12} className="me-1" />Completed</>
                      : <><Clock size={12} className="me-1" />{item.status}</>}
                  </span>
                  <small className="text-muted">
                    {item.scheduled_at ? new Date(item.scheduled_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'No date'}
                  </small>
                </div>

                <div className="card-body p-3">
                  {/* Lead Info */}
                  {item.lead_company && (
                    <div className="mb-2">
                      <span className="fw-bold text-white d-block">{item.lead_company}</span>
                      {item.lead_sector && <small className="text-muted">{item.lead_sector}</small>}
                    </div>
                  )}

                  {/* Action Notes */}
                  <h6 className="fw-bold text-info mb-2 small">📋 Follow-up Task:</h6>
                  <p className="small text-light mb-3" style={{ lineHeight: '1.5' }}>
                    {item.action || item.notes}
                  </p>

                  {/* ML Scores */}
                  {(item.lead_score != null || item.purchase_probability != null) && (
                    <div className="d-flex gap-2 mb-3">
                      {item.lead_score != null && (
                        <span className={`badge ${item.lead_score >= 70 ? 'bg-success' : item.lead_score >= 40 ? 'bg-warning text-dark' : 'bg-danger'} small`}>
                          ML Score: {item.lead_score}
                        </span>
                      )}
                      {item.purchase_probability != null && (
                        <span className="badge bg-primary small">
                          Conv: {(item.purchase_probability * 100).toFixed(0)}%
                        </span>
                      )}
                      {item.ai?.priority && (
                        <span className={`badge small ${priorityColor(item.ai.priority)}`}>
                          {item.ai.priority} Priority
                        </span>
                      )}
                    </div>
                  )}

                  {/* AI Next-Best-Action (collapsible) */}
                  {item.ai && (
                    <div className="border border-secondary rounded p-2 mb-3" style={{ backgroundColor: '#0f172a' }}>
                      <button
                        className="btn btn-sm w-100 text-start d-flex align-items-center justify-content-between p-0 border-0"
                        style={{ background: 'none', color: '#94a3b8' }}
                        onClick={() => toggleAI(item.id)}
                      >
                        <span className="d-flex align-items-center gap-1 fw-semibold small text-warning">
                          <Brain size={14} /> AI Next-Best-Action
                        </span>
                        {expandedAI[item.id] ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                      </button>

                      {expandedAI[item.id] && (
                        <div className="mt-2 pt-2 border-top border-secondary">
                          <p className="small text-light mb-2 fw-semibold">
                            <Target size={12} className="me-1 text-success" />
                            {item.ai.next_best_action}
                          </p>
                          <p className="small mb-2" style={{ color: '#94a3b8' }}>
                            <strong>Rationale:</strong> {item.ai.reason}
                          </p>
                          {item.ai.risk_level && (
                            <p className="small mb-1">
                              <strong>Risk: </strong>{riskIcon(item.ai.risk_level)}
                            </p>
                          )}
                          {item.ai.pricing_strategy && (
                            <p className="small mb-0" style={{ color: '#cbd5e1' }}>
                              <DollarSign size={11} className="me-1 text-warning" />
                              {item.ai.pricing_strategy}
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Card Footer Actions */}
                <div className="card-footer border-secondary d-flex align-items-center justify-content-between" style={{ backgroundColor: '#0f172a' }}>
                  {item.status !== 'completed' ? (
                    <button onClick={() => handleStatusUpdate(item.id, 'completed')} className="btn btn-sm btn-outline-success d-flex align-items-center gap-1">
                      <Check size={14} /> Mark Complete
                    </button>
                  ) : (
                    <span className="small text-success d-flex align-items-center gap-1"><CheckCircle2 size={14} /> Done</span>
                  )}
                  <button onClick={() => handleDelete(item.id)} className="btn btn-sm btn-outline-danger">
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Schedule Modal */}
      {showModal && (
        <div className="modal d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.7)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content border-secondary" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
              <div className="modal-header border-secondary">
                <h5 className="modal-title d-flex align-items-center gap-2">
                  <Sparkles size={20} className="text-warning" /> Schedule Follow-up Touchpoint
                </h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowModal(false)} />
              </div>
              <form onSubmit={handleCreate}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-light">Select Prospect Lead *</label>
                    <select
                      className="form-select bg-dark text-light border-secondary"
                      value={newFollowup.lead_id}
                      onChange={e => setNewFollowup({ ...newFollowup, lead_id: e.target.value })}
                      required
                    >
                      <option value="">-- Select Lead --</option>
                      {leads.map(l => (
                        <option key={l.id} value={l.id}>
                          {l.company} ({l.contact_name || l.email})
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-light">Action / Follow-up Details *</label>
                    <textarea
                      className="form-control bg-dark text-light border-secondary"
                      rows="3"
                      placeholder="e.g., Call CTO Sarah about Q3 pilot budget approval and propose SCADA demo..."
                      value={newFollowup.notes}
                      onChange={e => setNewFollowup({ ...newFollowup, notes: e.target.value })}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small fw-semibold text-light">Scheduled Date &amp; Time *</label>
                    <input
                      type="datetime-local"
                      className="form-control bg-dark text-light border-secondary"
                      value={newFollowup.follow_up_at}
                      onChange={e => setNewFollowup({ ...newFollowup, follow_up_at: e.target.value })}
                      required
                    />
                  </div>
                  <div className="alert alert-info border-0 small" style={{ backgroundColor: 'rgba(59,130,246,0.1)', color: '#93c5fd' }}>
                    <Brain size={14} className="me-1" />
                    <strong>AI-Powered:</strong> After scheduling, AI will automatically generate the Next-Best-Action recommendation for this lead based on ML scoring.
                  </div>
                </div>
                <div className="modal-footer border-secondary">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary d-flex align-items-center gap-1">
                    <Plus size={16} /> Schedule Task
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FollowUps;
