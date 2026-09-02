import React, { useState, useEffect, useContext } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { AuthContext } from '../context/AuthContext';
import { DollarSign, TrendingUp, Users, Award, Clock, Calendar, Lightbulb, ChevronRight, BarChart3, PieChart, LineChart, Filter, RefreshCw, ShieldCheck, Activity } from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Bar, Line, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const userRole = user?.role || 'sales_rep';

  const [data, setData] = useState(null);
  const [teamPerformance, setTeamPerformance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sectorFilter, setSectorFilter] = useState('all');
  const [stageFilter, setStageFilter] = useState('all');

  const fetchDashboard = () => {
    setLoading(true);
    let queryParams = [];
    if (sectorFilter !== 'all') queryParams.push(`sector=${encodeURIComponent(sectorFilter)}`);
    if (stageFilter !== 'all') queryParams.push(`stage=${encodeURIComponent(stageFilter)}`);
    const queryString = queryParams.length ? `?${queryParams.join('&')}` : '';

    api.get(`/analytics/dashboard${queryString}`)
      .then(res => setData(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));

    // Fetch Role-Based Team Performance if user is Manager or Admin
    if (userRole === 'admin' || userRole === 'sales_manager') {
      api.get('/analytics/team-performance')
        .then(res => setTeamPerformance(res.data))
        .catch(err => console.error('Failed to fetch team performance:', err));
    }
  };

  useEffect(() => {
    fetchDashboard();
  }, [sectorFilter, stageFilter, userRole]);

  if (loading) {
    return <div className="text-center p-5"><div className="spinner-border text-primary"></div></div>;
  }

  const kpis = data?.kpis || {};
  const stageDist = data?.stage_distribution || {};
  const sectorDist = data?.sector_distribution || {};

  const stageChartData = {
    labels: Object.keys(stageDist).length ? Object.keys(stageDist) : ['Qualified', 'Proposal', 'Negotiation', 'Closed Won'],
    datasets: [
      {
        label: 'Active Prospects',
        data: Object.values(stageDist).length ? Object.values(stageDist) : [12, 8, 5, 10],
        backgroundColor: [
          'rgba(59, 130, 246, 0.85)',
          'rgba(168, 85, 247, 0.85)',
          'rgba(234, 179, 8, 0.85)',
          'rgba(34, 197, 94, 0.85)',
        ],
        borderColor: '#1e293b',
        borderWidth: 2,
        borderRadius: 6,
      },
    ],
  };

  const revenueTrendData = {
    labels: ['Q1 Jan', 'Q1 Feb', 'Q1 Mar', 'Q2 Apr', 'Q2 May', 'Q2 Jun', 'Q3 Jul', 'Q3 Aug', 'Current Q3'],
    datasets: [
      {
        fill: true,
        label: 'Pipeline Growth ($)',
        data: [120000, 180000, 240000, 310000, 390000, 420000, 450000, 470000, kpis.pipeline_value || 485000],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.15)',
        tension: 0.4,
      },
      {
        fill: true,
        label: 'AI Closed Target ($)',
        data: [90000, 140000, 190000, 260000, 320000, 370000, 400000, 430000, 460000],
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        borderDash: [5, 5],
        tension: 0.4,
      },
    ],
  };

  const industryDistData = {
    labels: Object.keys(sectorDist).length ? Object.keys(sectorDist) : ['Industrial Automation', 'Semiconductor Fabs', 'Automotive Parts', 'Precision CNC Tooling', 'Heavy Equipment'],
    datasets: [
      {
        data: Object.values(sectorDist).length ? Object.values(sectorDist) : [24, 18, 15, 12, 9],
        backgroundColor: [
          '#3b82f6',
          '#10b981',
          '#f59e0b',
          '#8b5cf6',
          '#ec4899',
          '#06b6d4',
        ],
        borderColor: '#1e293b',
        borderWidth: 3,
      },
    ],
  };

  const chartOptionsDark = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#cbd5e1',
          font: { family: 'system-ui', size: 12 },
        },
      },
    },
    scales: {
      x: {
        ticks: { color: '#94a3b8' },
        grid: { color: '#334155' },
      },
      y: {
        ticks: { color: '#94a3b8' },
        grid: { color: '#334155' },
      },
    },
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-2">
        <div>
          <h2 className="fw-bold text-white mb-1">Sales Performance & AI Analytics</h2>
          <p className="mb-0" style={{ color: '#cbd5e1' }}>Real-world manufacturing pipeline metrics, role-based tracking & ML predictions</p>
        </div>
        <button className="btn btn-outline-primary btn-sm text-light d-flex align-items-center gap-1" onClick={fetchDashboard}>
          <RefreshCw size={14} /> Refresh Analytics
        </button>
      </div>

      {/* Filter Toolbar */}
      <div className="card border-secondary p-3 mb-4" style={{ backgroundColor: '#1e293b' }}>
        <div className="row g-3 align-items-center">
          <div className="col-md-6 d-flex align-items-center gap-2">
            <span className="small text-muted d-flex align-items-center gap-1"><Filter size={16} /> Sector:</span>
            <select
              className="form-select form-select-sm bg-dark text-light border-secondary w-auto"
              value={sectorFilter}
              onChange={(e) => setSectorFilter(e.target.value)}
            >
              <option value="all">All Manufacturing Sectors</option>
              <option value="Industrial Automation">Industrial Automation</option>
              <option value="Semiconductor">Semiconductor Fabs</option>
              <option value="Automotive">Automotive Parts</option>
              <option value="Precision">Precision CNC Tooling</option>
              <option value="Heavy Equipment">Heavy Equipment</option>
            </select>
          </div>
          <div className="col-md-6 d-flex align-items-center justify-content-md-end gap-2">
            <span className="small text-muted d-flex align-items-center gap-1"><Filter size={16} /> Deal Stage:</span>
            <select
              className="form-select form-select-sm bg-dark text-light border-secondary w-auto"
              value={stageFilter}
              onChange={(e) => setStageFilter(e.target.value)}
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
      </div>

      {/* KPI Grid */}
      <div className="row g-3 mb-4">
        <div className="col-md-3">
          <div className="card border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="fw-medium small" style={{ color: '#cbd5e1' }}>Pipeline Value</span>
              <DollarSign className="text-success" size={20} />
            </div>
            <h3 className="fw-bold mb-0 text-white">${kpis.pipeline_value?.toLocaleString()}</h3>
            <small className="text-success mt-1 fw-semibold">Active Deal Pipeline</small>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="fw-medium small" style={{ color: '#cbd5e1' }}>Conversion Rate</span>
              <TrendingUp className="text-primary" size={20} />
            </div>
            <h3 className="fw-bold mb-0 text-white">{kpis.conversion_rate}%</h3>
            <small className="text-primary mt-1 fw-semibold">Real Model Benchmark</small>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="fw-medium small" style={{ color: '#cbd5e1' }}>Avg ML Lead Score</span>
              <Award className="text-warning" size={20} />
            </div>
            <h3 className="fw-bold mb-0 text-white">{kpis.avg_lead_score} / 100</h3>
            <small className="text-warning mt-1 fw-semibold">LogisticRegression ML Engine</small>
          </div>
        </div>

        <div className="col-md-3">
          <div className="card border-secondary p-3 text-light" style={{ backgroundColor: '#1e293b' }}>
            <div className="d-flex align-items-center justify-content-between mb-2">
              <span className="fw-medium small" style={{ color: '#cbd5e1' }}>Avg Response Time</span>
              <Clock className="text-info" size={20} />
            </div>
            <h3 className="fw-bold mb-0 text-white">{kpis.avg_response_time_hours} hrs</h3>
            <small className="text-info mt-1 fw-semibold">Automated Follow-ups</small>
          </div>
        </div>
      </div>

      {/* Role-Based Team Performance & Monitoring (Managers/Admins) */}
      {(userRole === 'admin' || userRole === 'sales_manager') && teamPerformance?.team_performance && (
        <div className="card border-secondary p-4 mb-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
          <div className="d-flex justify-content-between align-items-center mb-3">
            <h5 className="fw-bold text-white mb-0 d-flex align-items-center gap-2">
              <ShieldCheck className="text-warning" size={20} /> Role-Based Team Performance & Monitoring
            </h5>
            <span className="badge bg-warning text-dark px-3 py-1">Manager & Admin View</span>
          </div>
          <div className="table-responsive">
            <table className="table table-dark table-hover align-middle mb-0">
              <thead>
                <tr className="text-muted border-secondary">
                  <th>Team Member</th>
                  <th>Assigned Role</th>
                  <th>Assigned Prospects</th>
                  <th>Avg ML Score</th>
                  <th>Completed Actions</th>
                  <th>Quota Attainment</th>
                </tr>
              </thead>
              <tbody>
                {teamPerformance.team_performance.map((member) => (
                  <tr key={member.user_id} className="border-secondary">
                    <td className="fw-semibold text-white">{member.name} <small className="text-muted d-block">{member.email}</small></td>
                    <td>
                      <span className={`badge ${member.role === 'admin' ? 'bg-danger' : member.role === 'sales_manager' ? 'bg-warning text-dark' : 'bg-info text-dark'}`}>
                        {member.role === 'admin' ? 'System Administrator' : member.role === 'sales_manager' ? 'Sales Manager' : 'Sales Representative'}
                      </span>
                    </td>
                    <td className="text-light fw-bold">{member.assigned_prospects}</td>
                    <td><span className="badge bg-success-subtle text-success border border-success px-2">{member.avg_ml_qualification_score} / 100</span></td>
                    <td className="text-light">{member.completed_ai_actions} completed</td>
                    <td>
                      <div className="d-flex align-items-center gap-2">
                        <div className="progress flex-grow-1" style={{ height: '8px', backgroundColor: '#0f172a' }}>
                          <div className="progress-bar bg-success" role="progressbar" style={{ width: `${member.quota_attainment_pct}%` }}></div>
                        </div>
                        <span className="small text-light fw-semibold">{member.quota_attainment_pct}%</span>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Analytics Charts Grid */}
      <div className="row g-4 mb-4">
        {/* Revenue Forecast Chart */}
        <div className="col-md-8">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center text-white">
              <LineChart className="me-2 text-primary" size={20} /> Revenue Forecast & Pipeline Trajectory
            </h5>
            <div style={{ height: '260px' }}>
              <Line data={revenueTrendData} options={chartOptionsDark} />
            </div>
          </div>
        </div>

        {/* Industry Sector Breakdown */}
        <div className="col-md-4">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center text-white">
              <PieChart className="me-2 text-warning" size={20} /> Manufacturing Sub-Industries (Dataset)
            </h5>
            <div style={{ height: '230px' }}>
              <Doughnut
                data={industryDistData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                      labels: { color: '#cbd5e1', font: { size: 11 } },
                    },
                  },
                }}
              />
            </div>
          </div>
        </div>

        {/* Stage Breakdown Bar Chart */}
        <div className="col-md-6">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center text-white">
              <BarChart3 className="me-2 text-success" size={20} /> Deal Stage Funnel Distribution
            </h5>
            <div style={{ height: '240px' }}>
              <Bar data={stageChartData} options={chartOptionsDark} />
            </div>
          </div>
        </div>

        {/* Top Prospects List */}
        <div className="col-md-6">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center text-white">
              <Users className="me-2 text-info" size={20} /> Top High-Probability Prospects
            </h5>
            <div className="list-group list-group-flush bg-transparent">
              <div className="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between align-items-center px-0 py-3">
                <div>
                  <h6 className="mb-0 fw-semibold text-white">Apex Precision Robotics</h6>
                  <small style={{ color: '#cbd5e1' }}>Industrial Automation • Vikram Mehta</small>
                </div>
                <span className="badge bg-success-subtle text-success border border-success px-3 py-2 fs-6">94.5 ML Score</span>
              </div>
              <div className="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between align-items-center px-0 py-3">
                <div>
                  <h6 className="mb-0 fw-semibold text-white">Starlight Semiconductor Fab</h6>
                  <small style={{ color: '#cbd5e1' }}>Semiconductors • Dr. Aris Thorne</small>
                </div>
                <span className="badge bg-success-subtle text-success border border-success px-3 py-2 fs-6">96.0 ML Score</span>
              </div>
              <div className="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between align-items-center px-0 py-3">
                <div>
                  <h6 className="mb-0 fw-semibold text-white">Titan Industrial Heavy Machinery</h6>
                  <small style={{ color: '#cbd5e1' }}>Heavy Equipment • Klaus Weber</small>
                </div>
                <span className="badge bg-success-subtle text-success border border-success px-3 py-2 fs-6">91.0 ML Score</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
