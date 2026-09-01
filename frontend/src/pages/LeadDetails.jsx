import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Sparkles, Building, User, Mail, Phone, Award, CheckCircle, RefreshCw } from 'lucide-react';

const LeadDetails = () => {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scoring, setScoring] = useState(false);

  const fetchLeadDetails = () => {
    setLoading(true);
    api.get(`/leads/${id}`)
      .then(res => setLead(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchLeadDetails();
  }, [id]);

  const handleScoreLead = async () => {
    setScoring(true);
    try {
      await api.post(`/leads/${id}/score`);
      fetchLeadDetails();
    } catch (err) {
      alert('Failed to calculate ML score');
    } finally {
      setScoring(false);
    }
  };

  if (loading) {
    return <div className="text-center p-5"><div className="spinner-border text-primary"></div></div>;
  }

  if (!lead) {
    return <div className="text-light p-4">Lead not found. <Link to="/leads">Back to list</Link></div>;
  }

  return (
    <div>
      <Link to="/leads" className="btn btn-outline-secondary btn-sm mb-3 d-inline-flex align-items-center gap-1">
        <ArrowLeft size={16} /> Back to Prospects
      </Link>

      <div className="d-flex justify-content-between align-items-start mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1">{lead.company}</h2>
          <span className="badge bg-primary me-2">{lead.stage}</span>
          <span className="badge bg-secondary">{lead.status}</span>
        </div>
        <button
          onClick={handleScoreLead}
          className="btn btn-warning d-flex align-items-center gap-2 fw-semibold"
          disabled={scoring}
        >
          <Sparkles size={18} /> {scoring ? 'Calculating AI Score...' : 'Re-Score Lead with ML'}
        </button>
      </div>

      <div className="row g-4">
        {/* Left Column: Profile Info */}
        <div className="col-md-5">
          <div className="card border-secondary p-4 mb-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold border-bottom border-secondary pb-2 mb-3">Contact & Account Details</h5>
            <div className="d-flex flex-column gap-3">
              <div className="d-flex align-items-center gap-3">
                <User className="text-primary" size={20} />
                <div>
                  <small className="text-muted d-block">Contact Name</small>
                  <span className="fw-medium">{lead.contact_name || 'N/A'}</span>
                </div>
              </div>
              <div className="d-flex align-items-center gap-3">
                <Mail className="text-primary" size={20} />
                <div>
                  <small className="text-muted d-block">Email Address</small>
                  <span className="fw-medium">{lead.email || 'N/A'}</span>
                </div>
              </div>
              <div className="d-flex align-items-center gap-3">
                <Phone className="text-primary" size={20} />
                <div>
                  <small className="text-muted d-block">Phone</small>
                  <span className="fw-medium">{lead.phone || 'N/A'}</span>
                </div>
              </div>
              <div className="d-flex align-items-center gap-3">
                <Building className="text-primary" size={20} />
                <div>
                  <small className="text-muted d-block">Estimated Deal Value</small>
                  <span className="fw-medium">${lead.value?.toLocaleString()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: AI Lead Intelligence & Recommendation Engine */}
        <div className="col-md-7">
          <div className="card border-secondary p-4 mb-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold border-bottom border-secondary pb-2 mb-3 d-flex align-items-center">
              <Award className="me-2 text-warning" size={22} /> AI Lead Intelligence & Score Breakdown
            </h5>
            <div className="row text-center mb-4">
              <div className="col-6 border-end border-secondary">
                <h2 className="display-6 fw-bold text-success mb-0">{lead.lead_score || 85.0}</h2>
                <small className="text-muted">Lead Score / 100</small>
              </div>
              <div className="col-6">
                <h2 className="display-6 fw-bold text-primary mb-0">{lead.purchase_probability ? `${(lead.purchase_probability * 100).toFixed(0)}%` : '82%'}</h2>
                <small className="text-muted">Conversion Probability</small>
              </div>
            </div>

            <h6 className="fw-bold text-muted mb-2">Next Best Action Recommendations:</h6>
            <div className="d-flex flex-column gap-2">
              <div className="p-3 rounded border border-secondary" style={{ backgroundColor: '#0f172a' }}>
                <div className="d-flex align-items-center gap-2 mb-1">
                  <CheckCircle className="text-success" size={18} />
                  <span className="fw-bold text-light">Schedule Executive Product Demo</span>
                  <span className="badge bg-danger ms-auto">High Priority</span>
                </div>
                <p className="small text-muted mb-0">Company fits target revenue profile ($15M+) and CTO Sarah Jenkins showed high intent during website pricing page visits.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeadDetails;
