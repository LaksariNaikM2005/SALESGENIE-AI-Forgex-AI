import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { DollarSign, TrendingUp, Users, Award, Clock, Activity } from 'lucide-react';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/analytics/dashboard')
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="text-center p-5"><div className="spinner-border text-primary"></div></div>;
  }

  const kpis = data?.kpis || {};
  const stageDist = data?.stage_distribution || {};

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1">Sales Performance Dashboard</h2>
          <p className="text-muted mb-0">Real-time pipeline metrics & AI conversion predictions</p>
        </div>
        <button className="btn btn-outline-primary btn-sm" onClick={() => window.location.reload()}>
          Refresh Analytics
        </button>
      </div>

      {/* KPI Grid */}
      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card bg-slate-800 border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="text-muted small">Pipeline Value</span>
              <DollarSign className="text-success" size={20} />
            </div>
            <h3 className="fw-bold mb-0">${kpis.pipeline_value?.toLocaleString()}</h3>
            <small className="text-success mt-1">Active Deal Pipeline</small>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card bg-slate-800 border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="text-muted small">Conversion Rate</span>
              <TrendingUp className="text-primary" size={20} />
            </div>
            <h3 className="fw-bold mb-0">{kpis.conversion_rate}%</h3>
            <small className="text-primary mt-1">+4.2% vs last month</small>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card bg-slate-800 border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="text-muted small">Avg Lead Score</span>
              <Award className="text-warning" size={20} />
            </div>
            <h3 className="fw-bold mb-0">{kpis.avg_lead_score} / 100</h3>
            <small className="text-warning mt-1">Random Forest Predictor</small>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card bg-slate-800 border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="text-muted small">Avg Response Time</span>
              <Clock className="text-info" size={20} />
            </div>
            <h3 className="fw-bold mb-0">{kpis.avg_response_time_hours} hrs</h3>
            <small className="text-info mt-1">Automated Follow-ups</small>
          </div>
        </div>
      </div>

      {/* Stage Breakdown & Pipeline Cards */}
      <div className="row g-4 mb-4">
        <div className="col-md-6">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center"><Activity className="me-2 text-primary" size={20} /> Deal Stage Breakdown</h5>
            <div className="d-flex flex-column gap-3">
              {Object.entries(stageDist).map(([stage, count]) => (
                <div key={stage}>
                  <div className="d-flex justify-content-between small mb-1">
                    <span>{stage}</span>
                    <span className="fw-bold">{count} leads</span>
                  </div>
                  <div className="progress" style={{ height: '8px', backgroundColor: '#0f172a' }}>
                    <div
                      className="progress-bar bg-primary"
                      role="progressbar"
                      style={{ width: `${Math.min(count * 10, 100)}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center"><Users className="me-2 text-success" size={20} /> Top High-Probability Prospects</h5>
            <div className="list-group list-group-flush bg-transparent">
              <div className="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between align-items-center px-0">
                <div>
                  <h6 className="mb-0 fw-semibold">Acme Tech Solutions</h6>
                  <small className="text-muted">Sarah Jenkins (CTO)</small>
                </div>
                <span className="badge bg-success-subtle text-success border border-success">88.5 ML Score</span>
              </div>
              <div className="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between align-items-center px-0">
                <div>
                  <h6 className="mb-0 fw-semibold">Global Logistics Corp</h6>
                  <small className="text-muted">David Miller (VP Ops)</small>
                </div>
                <span className="badge bg-success-subtle text-success border border-success">92.0 ML Score</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
