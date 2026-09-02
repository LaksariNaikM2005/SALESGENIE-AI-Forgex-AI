import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Calendar, Clock, CheckCircle2, AlertCircle, Plus, Sparkles, Filter, Trash2, Check } from 'lucide-react';

const FollowUps = () => {
  const [followups, setFollowups] = useState([]);
  const [filter, setFilter] = useState('all'); // all, pending, completed, cancelled
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [newFollowup, setNewFollowup] = useState({
    lead_id: '',
    notes: '',
    follow_up_at: new Date(Date.now() + 86400000 * 2).toISOString().slice(0, 16), // default +2 days
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
    api.get('/leads')
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

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1 d-flex align-items-center gap-2">
            <Calendar className="text-primary" size={28} /> Scheduled Follow-ups & Reminders
          </h2>
          <p className="text-muted mb-0">Track upcoming buyer touchpoints, schedule reminders, and mark tasks completed</p>
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
          <span className="small text-muted">Total Managed: {followups.length} Tasks</span>
        </div>
      </div>

      {/* Follow-ups List */}
      <div className="row g-3">
        {loading ? (
          <div className="col-12 text-center py-5"><div className="spinner-border text-primary"></div></div>
        ) : followups.length === 0 ? (
          <div className="col-12 text-center py-5 card border-secondary text-muted" style={{ backgroundColor: '#1e293b' }}>
            <Clock size={48} className="mx-auto mb-2 opacity-50 text-secondary" />
            <p>No follow-ups found for this filter. Click "Schedule Follow-up" to add one!</p>
          </div>
        ) : (
          followups.map((item) => (
            <div key={item.id} className="col-md-6 col-lg-4">
              <div className="card border-secondary h-100 p-3" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
                <div className="d-flex align-items-center justify-content-between mb-2">
                  <span className={`badge ${item.status === 'completed' ? 'bg-success' : 'bg-warning text-dark'} text-capitalize px-2 py-1`}>
                    {item.status === 'completed' ? <CheckCircle2 size={14} className="me-1" /> : <Clock size={14} className="me-1" />}
                    {item.status}
                  </span>
                  <small className="text-muted">{item.scheduled_at ? new Date(item.scheduled_at).toLocaleDateString() : 'No date'}</small>
                </div>

                <h6 className="fw-bold text-white mb-2">{item.action || item.notes}</h6>

                <div className="mt-auto pt-3 border-top border-secondary d-flex align-items-center justify-content-between">
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
                <h5 className="modal-title">Schedule Follow-up Touchpoint</h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleCreate}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label small text-muted">Select Prospect Lead</label>
                    <select
                      className="form-select bg-dark text-light border-secondary"
                      value={newFollowup.lead_id}
                      onChange={e => setNewFollowup({ ...newFollowup, lead_id: e.target.value })}
                      required
                    >
                      <option value="">-- Select Lead --</option>
                      {leads.map(l => (
                        <option key={l.id} value={l.id}>{l.company} ({l.contact_name || l.email})</option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Action / Follow-up Details</label>
                    <textarea
                      className="form-control bg-dark text-light border-secondary"
                      rows="3"
                      placeholder="e.g., Send updated pricing sheet and call CTO Sarah for feedback..."
                      value={newFollowup.notes}
                      onChange={e => setNewFollowup({ ...newFollowup, notes: e.target.value })}
                      required
                    ></textarea>
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Scheduled Date & Time</label>
                    <input
                      type="datetime-local"
                      className="form-control bg-dark text-light border-secondary"
                      value={newFollowup.follow_up_at}
                      onChange={e => setNewFollowup({ ...newFollowup, follow_up_at: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div className="modal-footer border-secondary">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Schedule Task</button>
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
