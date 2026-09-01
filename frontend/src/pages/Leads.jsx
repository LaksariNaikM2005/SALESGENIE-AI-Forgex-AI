import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Search, Plus, Sparkles, Filter, ChevronRight } from 'lucide-react';

const Leads = () => {
  const [leads, setLeads] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [newLead, setNewLead] = useState({
    company: '',
    contact_name: '',
    email: '',
    phone: '',
    stage: 'New Lead',
    value: 50000,
  });

  const fetchLeads = () => {
    setLoading(true);
    api.get(`/leads?search=${search}`)
      .then(res => setLeads(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLeads();
  }, [search]);

  const handleCreateLead = async (e) => {
    e.preventDefault();
    try {
      await api.post('/leads', newLead);
      setShowModal(false);
      fetchLeads();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to create lead');
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1">Lead Intelligence & Prospects</h2>
          <p className="text-muted mb-0">Manage prospects, company profiles, and AI qualification scores</p>
        </div>
        <button className="btn btn-primary d-flex align-items-center gap-2" onClick={() => setShowModal(true)}>
          <Plus size={18} /> Add New Lead
        </button>
      </div>

      {/* Filter & Search Toolbar */}
      <div className="card border-secondary p-3 mb-4" style={{ backgroundColor: '#1e293b' }}>
        <div className="row g-3">
          <div className="col-md-6">
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-muted"><Search size={18} /></span>
              <input
                type="text"
                className="form-control bg-dark text-light border-secondary"
                placeholder="Search by company, contact, or email..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Leads Table */}
      <div className="card border-secondary" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
        <div className="table-responsive">
          <table className="table table-dark table-hover align-middle mb-0">
            <thead>
              <tr className="text-muted border-secondary">
                <th>Company</th>
                <th>Contact</th>
                <th>Stage</th>
                <th>Est Value</th>
                <th>ML Score</th>
                <th>Probability</th>
                <th className="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className="text-center py-4"><div className="spinner-border text-primary"></div></td></tr>
              ) : leads.length === 0 ? (
                <tr><td colSpan="7" className="text-center py-4 text-muted">No leads found. Create your first lead to get started!</td></tr>
              ) : (
                leads.map((lead) => (
                  <tr key={lead.id} className="border-secondary">
                    <td className="fw-semibold">{lead.company}</td>
                    <td>
                      <div>{lead.contact_name || 'N/A'}</div>
                      <small className="text-muted">{lead.email}</small>
                    </td>
                    <td><span className="badge bg-primary-subtle text-primary border border-primary">{lead.stage}</span></td>
                    <td>${lead.value?.toLocaleString()}</td>
                    <td>
                      <span className={`badge ${lead.lead_score >= 70 ? 'bg-success' : 'bg-warning'} px-2 py-1`}>
                        {lead.lead_score ? `${lead.lead_score} / 100` : 'Unscored'}
                      </span>
                    </td>
                    <td>{lead.purchase_probability ? `${(lead.purchase_probability * 100).toFixed(1)}%` : 'N/A'}</td>
                    <td className="text-end">
                      <Link to={`/leads/${lead.id}`} className="btn btn-sm btn-outline-light">
                        Details <ChevronRight size={16} />
                      </Link>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal for Creating Lead */}
      {showModal && (
        <div className="modal d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.7)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content border-secondary" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
              <div className="modal-header border-secondary">
                <h5 className="modal-title">Register New Prospect</h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleCreateLead}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label small text-muted">Company Name</label>
                    <input
                      type="text"
                      className="form-control bg-dark text-light border-secondary"
                      value={newLead.company}
                      onChange={e => setNewLead({ ...newLead, company: e.target.value })}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Contact Name</label>
                    <input
                      type="text"
                      className="form-control bg-dark text-light border-secondary"
                      value={newLead.contact_name}
                      onChange={e => setNewLead({ ...newLead, contact_name: e.target.value })}
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Email</label>
                    <input
                      type="email"
                      className="form-control bg-dark text-light border-secondary"
                      value={newLead.email}
                      onChange={e => setNewLead({ ...newLead, email: e.target.value })}
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label small text-muted">Deal Value ($)</label>
                    <input
                      type="number"
                      className="form-control bg-dark text-light border-secondary"
                      value={newLead.value}
                      onChange={e => setNewLead({ ...newLead, value: parseFloat(e.target.value) })}
                    />
                  </div>
                </div>
                <div className="modal-footer border-secondary">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Create Lead</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Leads;
