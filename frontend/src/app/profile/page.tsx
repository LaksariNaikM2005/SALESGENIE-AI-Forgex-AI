"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import {
  User,
  ShieldCheck,
  Mail,
  Award,
  TrendingUp,
  Users,
  Target,
} from "lucide-react";

export default function ProfilePage() {
  const { user, token } = useAuth();
  const [teamPerformance, setTeamPerformance] = useState<any[]>([]);
  const [loadingTeam, setLoadingTeam] = useState<boolean>(false);

  useEffect(() => {
    if (user?.role === "admin" || user?.role === "sales_manager") {
      fetchTeamPerformance();
    }
  }, [user]);

  const fetchTeamPerformance = async () => {
    setLoadingTeam(true);
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const res = await axios.get("/api/analytics/team-performance", { headers });
      setTeamPerformance(res.data.team_performance || []);
    } catch (err) {
      console.error("Team performance fetch failed:", err);
    } finally {
      setLoadingTeam(false);
    }
  };

  const role = user?.role || "sales_rep";
  const roleLabel =
    role === "admin"
      ? "System Administrator"
      : role === "sales_manager"
      ? "Sales Director / Manager"
      : "Sales Representative";

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        <div className="mb-4">
          <h1 className="h3 fw-bold text-white mb-1">User Profile & Performance Monitoring</h1>
          <p className="text-secondary small mb-0">
            Account credentials, security role permissions, and sales quota monitoring.
          </p>
        </div>

        {/* User Card */}
        <div className="card bg-dark border-secondary p-4 mb-4">
          <div className="d-flex flex-wrap align-items-center gap-4">
            <div
              className="d-flex align-items-center justify-content-center rounded-circle bg-primary bg-opacity-25 text-primary fw-bold fs-2"
              style={{ width: "72px", height: "72px" }}
            >
              {user?.name ? user.name[0].toUpperCase() : "U"}
            </div>

            <div className="flex-grow-1">
              <h4 className="fw-bold text-white mb-1">{user?.name || "User"}</h4>
              <div className="text-secondary small d-flex align-items-center mb-2">
                <Mail size={14} className="me-1" /> {user?.email}
              </div>
              <span className={`badge ${role === "admin" ? "bg-danger" : role === "sales_manager" ? "bg-warning text-dark" : "bg-info text-dark"}`}>
                {roleLabel}
              </span>
            </div>

            <div className="p-3 rounded border border-secondary" style={{ backgroundColor: "#0f172a", minWidth: "200px" }}>
              <div className="text-secondary small">Quota Attainment</div>
              <div className="fw-bold text-success fs-4">{role === "sales_manager" ? "92.4%" : "84.0%"}</div>
              <span className="text-muted small">Target: $1.2M Annual</span>
            </div>
          </div>
        </div>

        {/* Team Performance Monitoring (Managers & Admins) */}
        {(role === "admin" || role === "sales_manager") && (
          <div className="card bg-dark border-secondary p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <div>
                <h5 className="fw-bold text-white mb-0 d-flex align-items-center">
                  <Users size={18} className="me-2 text-primary" /> Sales Team Performance & Quota Monitor
                </h5>
                <span className="text-secondary small">
                  Restricted to Sales Directors and System Administrators.
                </span>
              </div>
              <span className="badge bg-success">Active Real-Time Monitoring</span>
            </div>

            {loadingTeam ? (
              <div className="text-center py-4 text-secondary">
                <div className="spinner-border text-primary me-2" /> Loading team metrics...
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-dark table-hover align-middle mb-0">
                  <thead style={{ backgroundColor: "#1e293b" }}>
                    <tr className="text-secondary small">
                      <th className="ps-3">Team Member</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Assigned Prospects</th>
                      <th>Avg ML Qualification Score</th>
                      <th>Completed AI Actions</th>
                      <th>Quota Attainment</th>
                    </tr>
                  </thead>
                  <tbody>
                    {teamPerformance.map((m: any) => (
                      <tr key={m.user_id}>
                        <td className="ps-3 fw-bold text-white">{m.name}</td>
                        <td className="text-secondary small">{m.email}</td>
                        <td>
                          <span
                            className={`badge ${
                              m.role === "admin"
                                ? "bg-danger"
                                : m.role === "sales_manager"
                                ? "bg-warning text-dark"
                                : "bg-info text-dark"
                            }`}
                          >
                            {m.role}
                          </span>
                        </td>
                        <td className="fw-semibold text-white">{m.assigned_prospects}</td>
                        <td className="text-success fw-bold">{m.avg_ml_qualification_score} / 100</td>
                        <td>{m.completed_ai_actions}</td>
                        <td>
                          <div className="d-flex align-items-center gap-2">
                            <div className="progress flex-grow-1" style={{ height: "6px", width: "50px", backgroundColor: "#334155" }}>
                              <div
                                className="progress-bar bg-success"
                                role="progressbar"
                                style={{ width: `${m.quota_attainment_pct}%` }}
                              />
                            </div>
                            <span className="text-white small fw-bold">{m.quota_attainment_pct}%</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}
      </div>
    </NextMainLayout>
  );
}
