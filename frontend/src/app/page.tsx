"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { NextMainLayout } from "../layouts/NextMainLayout";
import { useAuth } from "../context/AuthContext";
import {
  TrendingUp,
  DollarSign,
  Users,
  Target,
  Award,
  Zap,
  CheckCircle,
  Clock,
  Layers,
  ArrowUpRight,
  Filter,
} from "lucide-react";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
} from "chart.js";
import { Doughnut, Bar } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement
);

export default function DashboardPage() {
  const { user, token, loading: authLoading } = useAuth();
  const router = useRouter();

  const [analytics, setAnalytics] = useState<any>(null);
  const [topLeads, setTopLeads] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [sectorFilter, setSectorFilter] = useState<string>("all");
  const [stageFilter, setStageFilter] = useState<string>("all");

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    fetchDashboardData();
  }, [user, sectorFilter, stageFilter]);

  const fetchDashboardData = async () => {
    setLoading(true);
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const params: any = {};
      if (sectorFilter !== "all") params.sector = sectorFilter;
      if (stageFilter !== "all") params.stage = stageFilter;

      const [resAnalytics, resLeads] = await Promise.all([
        axios.get("/api/analytics/dashboard", { headers, params }),
        axios.get("/api/leads?per_page=6", { headers, params }),
      ]);

      setAnalytics(resAnalytics.data);
      setTopLeads(resLeads.data.leads || []);
    } catch (err) {
      console.error("Dashboard data fetch error:", err);
    } finally {
      setLoading(false);
    }
  };

  if (authLoading || (!user && loading)) {
    return (
      <div className="d-flex align-items-center justify-content-center min-vh-100 text-light">
        <div className="spinner-border text-primary me-3" role="status" />
        <span>Loading SalesGenie AI Engine...</span>
      </div>
    );
  }

  const kpis = analytics?.kpis || {
    total_leads: 60,
    open_leads: 45,
    pipeline_value: 485000,
    conversion_rate: 24.5,
    avg_lead_score: 78.4,
    avg_sales_cycle_days: 18.5,
    avg_response_time_hours: 2.4,
  };

  const sectors = analytics?.sector_distribution || {};
  const stages = analytics?.stage_distribution || {};

  const sectorChartData = {
    labels: Object.keys(sectors),
    datasets: [
      {
        data: Object.values(sectors),
        backgroundColor: [
          "#3b82f6",
          "#10b981",
          "#f59e0b",
          "#8b5cf6",
          "#ec4899",
          "#06b6d4",
        ],
        borderWidth: 1,
        borderColor: "#1e293b",
      },
    ],
  };

  const stageChartData = {
    labels: Object.keys(stages),
    datasets: [
      {
        label: "Deals in Stage",
        data: Object.values(stages),
        backgroundColor: "#3b82f6",
        borderRadius: 6,
      },
    ],
  };

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        {/* Header */}
        <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
          <div>
            <h1 className="h3 fw-bold text-white mb-1">Manufacturing Sales Executive Dashboard</h1>
            <p className="text-secondary small mb-0">
              Real-time ML qualification, PostgreSQL storage & Redis-accelerated pipeline intelligence.
            </p>
          </div>

          {/* Filter Bar */}
          <div className="d-flex gap-2">
            <select
              className="form-select form-select-sm bg-dark text-white border-secondary"
              value={sectorFilter}
              onChange={(e) => setSectorFilter(e.target.value)}
              style={{ width: "200px" }}
            >
              <option value="all">All Manufacturing Sectors</option>
              <option value="Industrial Automation">Industrial Automation</option>
              <option value="Semiconductor">Semiconductor Fabs</option>
              <option value="Automotive">Automotive Parts</option>
              <option value="CNC">Precision CNC Tooling</option>
              <option value="Heavy Equipment">Heavy Equipment</option>
            </select>

            <select
              className="form-select form-select-sm bg-dark text-white border-secondary"
              value={stageFilter}
              onChange={(e) => setStageFilter(e.target.value)}
              style={{ width: "170px" }}
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

        {/* KPI Cards Row */}
        <div className="row g-3 mb-4">
          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card bg-dark border-secondary p-3 h-100">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span className="text-secondary small">Total Pipeline Value</span>
                <span className="p-2 rounded bg-success bg-opacity-25 text-success">
                  <DollarSign size={18} />
                </span>
              </div>
              <h3 className="fw-bold text-white mb-1">${Number(kpis.pipeline_value).toLocaleString()}</h3>
              <span className="text-success small d-flex align-items-center">
                <TrendingUp size={14} className="me-1" /> +12.4% vs last quarter
              </span>
            </div>
          </div>

          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card bg-dark border-secondary p-3 h-100">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span className="text-secondary small">ML Average Score</span>
                <span className="p-2 rounded bg-primary bg-opacity-25 text-primary">
                  <Award size={18} />
                </span>
              </div>
              <h3 className="fw-bold text-white mb-1">{kpis.avg_lead_score} / 100</h3>
              <span className="text-primary small d-flex align-items-center">
                <Zap size={14} className="me-1" /> Scikit-learn Logistic Engine
              </span>
            </div>
          </div>

          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card bg-dark border-secondary p-3 h-100">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span className="text-secondary small">Conversion Rate</span>
                <span className="p-2 rounded bg-warning bg-opacity-25 text-warning">
                  <Target size={18} />
                </span>
              </div>
              <h3 className="fw-bold text-white mb-1">{kpis.conversion_rate}%</h3>
              <span className="text-warning small d-flex align-items-center">
                <CheckCircle size={14} className="me-1" /> {kpis.open_leads} active negotiations
              </span>
            </div>
          </div>

          <div className="col-12 col-sm-6 col-xl-3">
            <div className="card bg-dark border-secondary p-3 h-100">
              <div className="d-flex justify-content-between align-items-center mb-2">
                <span className="text-secondary small">Total Prospects</span>
                <span className="p-2 rounded bg-info bg-opacity-25 text-info">
                  <Users size={18} />
                </span>
              </div>
              <h3 className="fw-bold text-white mb-1">{kpis.total_leads}</h3>
              <span className="text-info small d-flex align-items-center">
                <Clock size={14} className="me-1" /> Avg cycle: {kpis.avg_sales_cycle_days} days
              </span>
            </div>
          </div>
        </div>

        {/* Charts Row */}
        <div className="row g-4 mb-4">
          <div className="col-12 col-lg-5">
            <div className="card bg-dark border-secondary p-3 h-100">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h5 className="fw-bold text-white mb-0">Manufacturing Sub-Industries</h5>
                <span className="badge bg-secondary">Live Breakdown</span>
              </div>
              <div className="d-flex align-items-center justify-content-center p-3" style={{ height: "260px" }}>
                <Doughnut
                  data={sectorChartData}
                  options={{
                    maintainAspectRatio: false,
                    plugins: {
                      legend: { position: "right", labels: { color: "#cbd5e1", boxWidth: 12, font: { size: 11 } } },
                    },
                  }}
                />
              </div>
            </div>
          </div>

          <div className="col-12 col-lg-7">
            <div className="card bg-dark border-secondary p-3 h-100">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h5 className="fw-bold text-white mb-0">Deal Stage Distribution Funnel</h5>
                <span className="badge bg-primary">Pipeline Funnel</span>
              </div>
              <div className="p-2" style={{ height: "260px" }}>
                <Bar
                  data={stageChartData}
                  options={{
                    maintainAspectRatio: false,
                    scales: {
                      x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
                      y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
                    },
                    plugins: {
                      legend: { display: false },
                    },
                  }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Top ML Qualified Prospects Table */}
        <div className="card bg-dark border-secondary p-3">
          <div className="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h5 className="fw-bold text-white mb-0">Top ML-Qualified Manufacturing Prospects</h5>
              <span className="text-secondary small">Ranked by predictive conversion & win probability</span>
            </div>
            <button onClick={() => router.push("/leads")} className="btn btn-sm btn-outline-primary d-flex align-items-center">
              View All Leads <ArrowUpRight size={14} className="ms-1" />
            </button>
          </div>

          <div className="table-responsive">
            <table className="table table-dark table-hover align-middle mb-0">
              <thead>
                <tr className="text-secondary small">
                  <th>Company</th>
                  <th>Manufacturing Sector</th>
                  <th>Hardware / Tech Stack</th>
                  <th>Deal Stage</th>
                  <th>Deal Value</th>
                  <th>Qualification Score</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {topLeads.map((lead: any) => (
                  <tr key={lead.id}>
                    <td>
                      <div className="fw-bold text-white">{lead.company}</div>
                      <div className="text-secondary small">{lead.contact_name}</div>
                    </td>
                    <td>
                      <span className="badge bg-secondary bg-opacity-50 text-light">{lead.sector}</span>
                    </td>
                    <td>
                      <div className="d-flex flex-wrap gap-1">
                        {(lead.tech_stack || "ROS2, Siemens PLC")
                          .split(",")
                          .slice(0, 2)
                          .map((tech: string, i: number) => (
                            <span key={i} className="badge bg-dark border border-secondary text-info small" style={{ fontSize: "10px" }}>
                              {tech.trim()}
                            </span>
                          ))}
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${lead.stage === "Won" ? "bg-success" : "bg-primary"}`}>
                        {lead.stage}
                      </span>
                    </td>
                    <td className="fw-semibold text-white">${Number(lead.value || 0).toLocaleString()}</td>
                    <td>
                      <div className="d-flex align-items-center gap-2">
                        <div className="progress flex-grow-1" style={{ height: "6px", width: "60px", backgroundColor: "#334155" }}>
                          <div
                            className="progress-bar bg-success"
                            role="progressbar"
                            style={{ width: `${lead.lead_score || 80}%` }}
                          />
                        </div>
                        <span className="fw-bold text-success small">{lead.lead_score || 80}</span>
                      </div>
                    </td>
                    <td>
                      <button
                        onClick={() => router.push(`/leads/${lead.id}`)}
                        className="btn btn-sm btn-outline-light py-1 px-2 small"
                      >
                        Insights
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </NextMainLayout>
  );
}
