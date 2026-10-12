import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';
import { Search, Plus, Sparkles, Filter, ChevronRight, Users, CheckCircle, RefreshCw, ChevronLeft, Cpu, DollarSign, Building, Trash2 } from 'lucide-react';

const Leads = () => {
  const { user } = useContext(AuthContext);
  const userRole = user?.role || 'sales_rep';

  const [leads, setLeads] = useState([]);
  const [search, setSearch] = useState('');
  const [sectorFilter, setSectorFilter] = useState('all');
  const [stageFilter, setStageFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalLeads, setTotalLeads] = useState(0);

  const [newLead, setNewLead] = useState({
    company: '',
    contact_name: '',
    email: '',
    phone: '',
    sector: 'Industrial Automation',
    product: 'Robotic Assembly Cell X7',
    tech_stack: 'ROS2, Siemens S7 PLC, Fanuc CNC, SCADA',
    revenue: 85,
    employees: 1450,
    stage: 'New Lead',
    value: 125000,
  });

  const fetchLeads = () => {
    setLoading(true);
    let queryParams = [`page=${page}`, `per_page=20`];
    if (search) queryParams.push(`search=${encodeURIComponent(search)}`);
    if (sectorFilter !== 'all') queryParams.push(`sector=${encodeURIComponent(sectorFilter)}`);
    if (stageFilter !== 'all') queryParams.push(`stage=${encodeURIComponent(stageFilter)}`);
    const queryString = `?${queryParams.join('&')}`;

    api.get(`/leads${queryString}`)
      .then(res => {
        let fetchedList = [];
        let totalCount = 0;
        let pagesCount = 1;

        if (res.data && Array.isArray(res.data.leads)) {
          fetchedList = res.data.leads;
          totalCount = res.data.total || res.data.leads.length;
          pagesCount = res.data.pages || 1;
        } else if (Array.isArray(res.data)) {
          fetchedList = res.data;
          totalCount = res.data.length;
        }

        setLeads(fetchedList);
        setTotalLeads(totalCount);
        setTotalPages(pagesCount);
      })
      .catch(err => {
        console.error('Failed to fetch leads:', err);
        setLeads([]);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLeads();
  }, [search, sectorFilter, stageFilter, page]);

  const handleCreateLead = async (e) => {
    e.preventDefault();
    try {
      await api.post('/leads', newLead);
      setShowModal(false);
      setNewLead({
        company: '',
        contact_name: '',
        email: '',
        phone: '',
        sector: 'Industrial Automation',
        product: 'Robotic Assembly Cell X7',
        tech_stack: 'ROS2, Siemens S7 PLC, Fanuc CNC, SCADA',
        revenue: 85,
        employees: 1450,
        stage: 'New Lead',
        value: 125000,
      });
      fetchLeads();
    } catch (err) {
      alert(err.response?.data?.error || err.response?.data?.message || 'Failed to create lead');
    }
  };

  const handleSyncDataset = async () => {
    if (userRole !== 'admin') {
      alert("RBAC Restricted: Only System Administrators can trigger global dataset synchronization.");
      return;
    }
    setSyncing(true);
    try {
      const res = await api.post('/leads/sync-real-dataset');
      alert(res.data?.message || 'Successfully synchronized 5,000 dataset records!');
      setPage(1);
      fetchLeads();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to synchronize dataset');
    } finally {
      setSyncing(false);
    }
  };

  const handleDeleteLead = async (id, company) => {
    if (userRole === 'sales_rep') {
      alert("RBAC Restricted: Sales Representatives cannot delete prospects. Contact your Sales Manager or Admin.");
      return;
    }
    if (!window.confirm(`Are you sure you want to delete prospect '${company}'?`)) {
      return;
    }
    try {
      await api.delete(`/leads/${id}`);
      fetchLeads();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete prospect');
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <div>
          <h2 className="fw-bold text-light mb-1 d-flex align-items-center gap-2">
            <Users className="text-primary" size={28} /> Lead Intelligence & Prospects
          </h2>
          <p className="text-muted mb-0">Browse real-world B2B manufacturing dataset prospects & ML qualification scores</p>
        </div>
        <div className="d-flex align-items-center gap-2">
          {userRole === 'admin' && (
            <button className="btn btn-outline-warning d-flex align-items-center gap-2" onClick={handleSyncDataset} disabled={syncing}>
              <RefreshCw size={16} className={syncing ? 'spin' : ''} /> {syncing ? 'Syncing 5,000 Records...' : 'Sync Full Dataset (Admin Only)'}
            </button>
          )}
          <button className="btn btn-primary d-flex align-items-center gap-2" onClick={() => setShowModal(true)}>
            <Plus size={18} /> Add New Lead
          </button>
        </div>
      </div>

      {/* Filter & Search Toolbar */}
      <div className="card border-secondary p-3 mb-4" style={{ backgroundColor: '#1e293b' }}>
        <div className="row g-3 align-items-center">
          <div className="col-md-4">
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-muted"><Search size={18} /></span>
              <input
                type="text"
                className="form-control bg-dark text-light border-secondary"
                placeholder="Search by company, contact, or email..."
                value={search}
                onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              />
            </div>
          </div>
          <div className="col-md-3">
            <div className="d-flex align-items-center gap-2">
              <span className="small text-muted d-flex align-items-center gap-1"><Filter size={14} /> Sector:</span>
              <select
                className="form-select form-select-sm bg-dark text-light border-secondary"
                value={sectorFilter}
                onChange={(e) => { setSectorFilter(e.target.value); setPage(1); }}
              >
                <option value="all">All Sectors</option>
                <option value="Industrial Automation">Industrial Automation</option>
                <option value="Automotive">Automotive Manufacturing</option>
                <option value="Chemical">Chemical Manufacturing</option>
                <option value="Heavy Equipment">Heavy Equipment</option>
                <option value="Metals">Metals Manufacturing</option>
                <option value="Machinery">Machinery</option>
                <option value="Aerospace">Aerospace Manufacturing</option>
                <option value="Tooling">Tooling Manufacturing</option>
                <option value="Semiconductor">Semiconductor Manufacturing</option>
              </select>
            </div>
          </div>
          <div className="col-md-3">
            <div className="d-flex align-items-center gap-2">
              <span className="small text-muted d-flex align-items-center gap-1"><Filter size={14} /> Stage:</span>
              <select
                className="form-select form-select-sm bg-dark text-light border-secondary"
                value={stageFilter}
                onChange={(e) => { setStageFilter(e.target.value); setPage(1); }}
              >
                <option value="all">All Stages</option>
                <option value="New Lead">New Lead</option>
                <option value="Qualified">Qualified</option>
                <option value="Proposal">Proposal</option>
                <option value="Negotiation">Negotiation</option>
                <option value="Won">Closed Won</option>
              </select>
            </div>
          </div>
          <div className="col-md-2 text-md-end text-muted small">
            <span>Total: <strong className="text-light">{totalLeads.toLocaleString()}</strong></span>
          </div>
        </div>
      </div>

      {/* Leads Table */}
      <div className="card border-secondary" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
        <div className="table-responsive">
          <table className="table table-dark table-hover align-middle mb-0">
            <thead>
              <tr className="text-muted border-secondary">
                <th style={{ color: '#cbd5e1' }}>#</th>
                <th style={{ color: '#cbd5e1' }}>Company</th>
                <th style={{ color: '#cbd5e1' }}>Contact & Sector</th>
                <th style={{ color: '#cbd5e1' }}>Tech Stack</th>
                <th style={{ color: '#cbd5e1' }}>Stage</th>
                <th style={{ color: '#cbd5e1' }}>Est Value</th>
                <th style={{ color: '#cbd5e1' }}>ML Score</th>
                <th className="text-end" style={{ color: '#cbd5e1' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="8" className="text-center py-4"><div className="spinner-border text-primary"></div></td></tr>
              ) : leads.length === 0 ? (
                <tr><td colSpan="8" className="text-center py-4 text-muted">No prospects match your filter criteria.</td></tr>
              ) : (
                leads.map((lead, idx) => (
                  <tr key={lead.id} className="border-secondary">
                    <td className="text-muted small">{(page - 1) * 20 + idx + 1}</td>
                    <td>
                      <div className="fw-semibold text-white">{lead.company}</div>
                      <small className="text-muted">{lead.product || 'Industrial Solution'}</small>
                    </td>
                    <td>
                      <div className="text-light">{lead.contact_name || 'N/A'}</div>
                      <span className="badge bg-dark border border-secondary text-info px-2 py-0">{lead.sector || 'Manufacturing'}</span>
                    </td>
                    <td>
                      <div className="d-flex flex-wrap gap-1" style={{ maxWidth: '240px' }}>
                        {(lead.tech_stack || "Siemens PLC, ROS2").split(',').map((tech, i) => (
                          <span key={i} className="badge border border-info-subtle px-2 py-1 d-inline-flex align-items-center" style={{ fontSize: '0.72rem', backgroundColor: '#0f172a', color: '#38bdf8' }}>
                            <Cpu size={11} className="me-1 text-warning flex-shrink-0" />{tech.trim()}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td><span className="badge bg-primary-subtle text-primary border border-primary px-2 py-1">{lead.stage}</span></td>
                    <td className="text-light">${lead.value ? lead.value.toLocaleString() : '125,000'}</td>
                    <td>
                      <span className={`badge ${lead.lead_score >= 70 ? 'bg-success' : lead.lead_score >= 40 ? 'bg-warning text-dark' : 'bg-danger'} px-2 py-1`}>
                        {lead.lead_score !== null && lead.lead_score !== undefined ? `${lead.lead_score} / 100` : 'Unscored'}
                      </span>
                    </td>
                    <td className="text-end">
                      <div className="d-inline-flex gap-1">
                        <Link to={`/leads/${lead.id}`} className="btn btn-sm btn-outline-light">
                          Details <ChevronRight size={16} />
                        </Link>
                        {userRole !== 'sales_rep' && (
                          <button
                            onClick={() => handleDeleteLead(lead.id, lead.company)}
                            className="btn btn-sm btn-outline-danger"
                            title="Delete Prospect (Manager/Admin Only)"
                          >
                            <Trash2 size={14} />
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        {totalPages > 1 && (
          <div className="card-footer border-secondary d-flex justify-content-between align-items-center py-3" style={{ backgroundColor: '#1e293b' }}>
            <button
              className="btn btn-sm btn-outline-secondary text-light d-flex align-items-center gap-1"
              disabled={page <= 1}
              onClick={() => setPage(p => Math.max(1, p - 1))}
            >
              <ChevronLeft size={16} /> Previous
            </button>
            <span className="small text-muted">Page {page} of {totalPages} ({totalLeads.toLocaleString()} prospects)</span>
            <button
              className="btn btn-sm btn-outline-secondary text-light d-flex align-items-center gap-1"
              disabled={page >= totalPages}
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            >
              Next <ChevronRight size={16} />
            </button>
          </div>
        )}
      </div>

      {/* Lead Registration Modal */}
      {showModal && (
        <div className="modal d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.7)' }}>
          <div className="modal-dialog modal-dialog-centered modal-lg">
            <div className="modal-content border-secondary" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
              <div className="modal-header border-secondary">
                <h5 className="modal-title d-flex align-items-center gap-2 text-white">
                  <Building size={20} className="text-primary" /> Register New Manufacturing Prospect
                </h5>
                <button type="button" className="btn-close btn-close-white" onClick={() => setShowModal(false)}></button>
              </div>
              <form onSubmit={handleCreateLead}>
                <div className="modal-body">
                  <div className="row g-3">
                    <div className="col-md-6">
                      <label className="form-label small fw-medium text-light">Company Name *</label>
                      <input
                        type="text"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.company}
                        onChange={e => setNewLead({ ...newLead, company: e.target.value })}
                        placeholder="e.g. Apex Precision Robotics"
                        required
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-medium text-light">Contact Name</label>
                      <input
                        type="text"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.contact_name}
                        onChange={e => setNewLead({ ...newLead, contact_name: e.target.value })}
                        placeholder="e.g. Vikram Mehta (VP Ops)"
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-medium text-light">Email Address</label>
                      <input
                        type="email"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.email}
                        onChange={e => setNewLead({ ...newLead, email: e.target.value })}
                        placeholder="contact@company.com"
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-medium text-light">Phone Number</label>
                      <input
                        type="text"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.phone}
                        onChange={e => setNewLead({ ...newLead, phone: e.target.value })}
                        placeholder="+1-555-882-1920"
                      />
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-medium text-light">Manufacturing Sector *</label>
                      <select
                        className="form-select bg-dark text-light border-secondary"
                        value={newLead.sector}
                        onChange={e => setNewLead({ ...newLead, sector: e.target.value })}
                      >
                        <option value="Industrial Automation">Industrial Automation & Robotics</option>
                        <option value="Semiconductor Fabs">Semiconductor Manufacturing</option>
                        <option value="Automotive Parts">Automotive Parts & Assemblies</option>
                        <option value="Precision CNC Tooling">Precision CNC Tooling</option>
                        <option value="Heavy Equipment">Heavy Machinery & Equipment</option>
                        <option value="Electronics Assembly">Electronics & Components</option>
                      </select>
                    </div>
                    <div className="col-md-6">
                      <label className="form-label small fw-medium text-light">Product Line</label>
                      <input
                        type="text"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.product}
                        onChange={e => setNewLead({ ...newLead, product: e.target.value })}
                        placeholder="e.g. Robotic Assembly Cell X7"
                      />
                    </div>
                    <div className="col-md-12">
                      <label className="form-label small fw-medium text-light">Technology Stack</label>
                      <input
                        type="text"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.tech_stack}
                        onChange={e => setNewLead({ ...newLead, tech_stack: e.target.value })}
                        placeholder="e.g. ROS2, Siemens S7 PLC, Fanuc CNC, EUV Lithography, MES, SCADA"
                      />
                    </div>
                    <div className="col-md-4">
                      <label className="form-label small fw-medium text-light">Annual Revenue ($M)</label>
                      <input
                        type="number"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.revenue}
                        onChange={e => setNewLead({ ...newLead, revenue: parseFloat(e.target.value) })}
                      />
                    </div>
                    <div className="col-md-4">
                      <label className="form-label small fw-medium text-light">Employee Count</label>
                      <input
                        type="number"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.employees}
                        onChange={e => setNewLead({ ...newLead, employees: parseInt(e.target.value) })}
                      />
                    </div>
                    <div className="col-md-4">
                      <label className="form-label small fw-medium text-light">Est Deal Value ($)</label>
                      <input
                        type="number"
                        className="form-control bg-dark text-light border-secondary"
                        value={newLead.value}
                        onChange={e => setNewLead({ ...newLead, value: parseFloat(e.target.value) })}
                      />
                    </div>
                  </div>
                </div>
                <div className="modal-footer border-secondary">
                  <button type="button" className="btn btn-outline-secondary" onClick={() => setShowModal(false)}>Cancel</button>
                  <button type="submit" className="btn btn-primary">Register Prospect & Predict ML Score</button>
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
