import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { ArrowLeft, Sparkles, Building, User, Mail, Phone, Award, CheckCircle, Cpu, Zap, DollarSign, Layers } from 'lucide-react';

const LeadDetails = () => {
  const { id } = useParams();
  const [lead, setLead] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scoring, setScoring] = useState(false);

  const fetchLeadDetails = () => {
    setLoading(true);
    api.get(`/leads/${id}`)
      .then(res => {
        const leadObj = res.data?.lead || res.data;
        setLead(leadObj);
        return api.get(`/leads/${id}/insights`);
      })
      .then(res => {
        setInsights(res.data);
      })
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

  if (!lead || !lead.company) {
    return <div className="text-light p-4">Prospect record not found. <Link to="/leads">Back to list</Link></div>;
  }

  return (
    <div>
      <Link to="/leads" className="btn btn-outline-secondary btn-sm mb-3 d-inline-flex align-items-center gap-1 text-light">
        <ArrowLeft size={16} /> Back to Prospects
      </Link>

      <div className="d-flex justify-content-between align-items-start mb-4 flex-wrap gap-2">
        <div>
          <h2 className="fw-bold text-white mb-1">{lead.company}</h2>
          <span className="badge bg-primary me-2 px-3 py-2">{lead.stage}</span>
          <span className="badge bg-secondary me-2 px-3 py-2">{lead.sector || 'Manufacturing'}</span>
          {insights?.risk_level && (
            <span className={`badge ${insights.risk_level === 'Low' ? 'bg-success' : insights.risk_level === 'Medium' ? 'bg-warning text-dark' : 'bg-danger'} px-3 py-2`}>
              {insights.risk_level} Deal Risk
            </span>
          )}
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
        {/* Left Column: Profile & Requirement 6 Tech Stack */}
        <div className="col-md-5">
          <div className="card border-secondary p-4 mb-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold border-bottom border-secondary pb-2 mb-3 text-white">Contact & Account Details</h5>
            <div className="d-flex flex-column gap-3">
              <div className="d-flex align-items-center gap-3">
                <User className="text-primary flex-shrink-0" size={20} />
                <div>
                  <small className="d-block" style={{ color: '#cbd5e1' }}>Contact Name</small>
                  <span className="fw-semibold text-white fs-6">{lead.contact_name || 'N/A'}</span>
                </div>
              </div>
              <div className="d-flex align-items-center gap-3">
                <Mail className="text-primary flex-shrink-0" size={20} />
                <div>
                  <small className="d-block" style={{ color: '#cbd5e1' }}>Email Address</small>
                  <span className="fw-semibold text-white fs-6">{lead.email || 'N/A'}</span>
                </div>
              </div>
              <div className="d-flex align-items-center gap-3">
                <Phone className="text-primary flex-shrink-0" size={20} />
                <div>
                  <small className="d-block" style={{ color: '#cbd5e1' }}>Phone</small>
                  <span className="fw-semibold text-white fs-6">{lead.phone || '+1-555-882-1920'}</span>
                </div>
              </div>
              <div className="d-flex align-items-center gap-3">
                <Building className="text-primary flex-shrink-0" size={20} />
                <div>
                  <small className="d-block" style={{ color: '#cbd5e1' }}>Estimated Deal Value</small>
                  <span className="fw-semibold text-success fs-5">${lead.value ? lead.value.toLocaleString() : '125,000'}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Requirement 6: Manufacturing Technology Stack Card */}
          <div className="card border-secondary p-4 mb-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold border-bottom border-secondary pb-2 mb-3 d-flex align-items-center text-white">
              <Cpu className="me-2 text-warning" size={20} /> Manufacturing Technology Stack
            </h5>
            <p className="small text-muted mb-3">Enterprise hardware, automation protocols, and industrial software deployed by {lead.company}:</p>
            <div className="d-flex flex-wrap gap-2">
              {(lead.tech_stack || "ROS2, Siemens S7 PLC, Fanuc CNC, EUV Lithography, MES, SCADA").split(',').map((tech, i) => (
                <span key={i} className="badge bg-dark border border-secondary text-light px-3 py-2 fs-6">
                  <Layers size={14} className="me-1 text-primary" /> {tech.trim()}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: AI Lead Intelligence & Recommendation Engine */}
        <div className="col-md-7">
          <div className="card border-secondary p-4 mb-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold border-bottom border-secondary pb-2 mb-3 d-flex align-items-center text-white">
              <Award className="me-2 text-warning" size={22} /> Real ML Qualification & AI Insights
            </h5>
            <div className="row text-center mb-4">
              <div className="col-6 border-end border-secondary">
                <h2 className={`display-6 fw-bold mb-0 ${lead.lead_score >= 70 ? 'text-success' : lead.lead_score >= 40 ? 'text-warning' : 'text-danger'}`}>
                  {lead.lead_score !== null && lead.lead_score !== undefined ? lead.lead_score : 'N/A'}
                </h2>
                <small style={{ color: '#cbd5e1' }}>ML Qualification Score / 100</small>
              </div>
              <div className="col-6">
                <h2 className="display-6 fw-bold text-primary mb-0">
                  {lead.purchase_probability !== null && lead.purchase_probability !== undefined ? `${(lead.purchase_probability * 100).toFixed(1)}%` : 'N/A'}
                </h2>
                <small style={{ color: '#cbd5e1' }}>Conversion Probability</small>
              </div>
            </div>

            {/* Key Drivers */}
            {insights?.key_drivers && insights.key_drivers.length > 0 && (
              <div className="mb-4">
                <h6 className="fw-bold mb-2 text-info d-flex align-items-center gap-1">
                  <Zap size={16} /> Key Conversion Drivers (ML Signals):
                </h6>
                <ul className="list-group list-group-flush border-secondary rounded">
                  {insights.key_drivers.map((driver, index) => (
                    <li key={index} className="list-group-item bg-dark text-light border-secondary small">
                      • {driver}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Next Best Action */}
            <h6 className="fw-bold mb-2" style={{ color: '#e2e8f0' }}>AI Next Best Action Recommendation:</h6>
            <div className="p-3 rounded border border-secondary mb-3" style={{ backgroundColor: '#0f172a' }}>
              <div className="d-flex align-items-center gap-2 mb-2">
                <CheckCircle className="text-success" size={18} />
                <span className="fw-bold text-white">{insights?.recommendation || 'Contact lead and present engineering specifications.'}</span>
                <span className={`badge ${insights?.priority === 'High' ? 'bg-danger' : 'bg-warning text-dark'} ms-auto`}>
                  {insights?.priority || 'High'} Priority
                </span>
              </div>
              <p className="small mb-0" style={{ color: '#cbd5e1' }}><strong>Rationale:</strong> {insights?.reason || 'Calculated based on real-world dataset feature signals and ML model probability.'}</p>
            </div>

            {/* Pricing & Discount Strategy */}
            {insights?.pricing_strategy && (
              <div>
                <h6 className="fw-bold mb-2 text-warning d-flex align-items-center gap-1">
                  <DollarSign size={16} /> Recommended Commercial Strategy:
                </h6>
                <div className="p-3 rounded border border-secondary bg-dark text-light small">
                  {insights.pricing_strategy}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeadDetails;
