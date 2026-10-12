"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import {
  Lightbulb,
  CheckCircle,
  AlertTriangle,
  Clock,
  ArrowRight,
  Filter,
  Check,
  Zap,
} from "lucide-react";

export default function RecommendationsPage() {
  const { token } = useAuth();
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchRecommendations();
  }, [priorityFilter]);

  const fetchRecommendations = async () => {
    setLoading(true);
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const params: any = {};
      if (priorityFilter !== "all") params.priority = priorityFilter;

      const res = await axios.get("/api/recommendations", { headers, params });
      setRecommendations(res.data.recommendations || []);
    } catch (err) {
      console.error("Failed to fetch recommendations:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleResolve = async (id: number, currentCompleted: boolean) => {
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      await axios.put(`/api/recommendations/${id}`, { completed: !currentCompleted }, { headers });
      setRecommendations((prev) =>
        prev.map((r) => (r.id === id ? { ...r, completed: !currentCompleted } : r))
      );
    } catch (err) {
      console.error("Failed to resolve recommendation:", err);
    }
  };

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
          <div>
            <h1 className="h3 fw-bold text-white mb-1">AI Recommendation Engine</h1>
            <p className="text-secondary small mb-0">
              Machine learning prioritization cards driving next-best-action sales velocity.
            </p>
          </div>

          <div className="d-flex gap-2">
            {["all", "High", "Medium", "Low"].map((p) => (
              <button
                key={p}
                onClick={() => setPriorityFilter(p)}
                className={`btn btn-sm ${
                  priorityFilter === p ? "btn-primary fw-semibold" : "btn-outline-secondary text-secondary"
                }`}
              >
                {p === "all" ? "All Priorities" : `${p} Priority`}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center py-5 text-secondary">
            <div className="spinner-border text-primary me-2" /> Generating recommendation cards...
          </div>
        ) : recommendations.length === 0 ? (
          <div className="alert alert-secondary">No recommendations found for current filter.</div>
        ) : (
          <div className="row g-3">
            {recommendations.map((rec) => {
              const badgeClass =
                rec.priority === "High"
                  ? "bg-danger"
                  : rec.priority === "Medium"
                  ? "bg-warning text-dark"
                  : "bg-info text-dark";

              return (
                <div key={rec.id} className="col-12 col-md-6 col-xl-4">
                  <div
                    className={`card bg-dark border-secondary p-3 h-100 position-relative ${
                      rec.completed ? "opacity-75" : ""
                    }`}
                    style={{ transition: "all 0.2s" }}
                  >
                    <div className="d-flex justify-content-between align-items-start mb-2">
                      <span className={`badge ${badgeClass} small`}>{rec.priority} Impact</span>
                      <span className="badge bg-secondary bg-opacity-50 text-light">{rec.sector}</span>
                    </div>

                    <h5 className="fw-bold text-white mb-1">{rec.lead_company}</h5>
                    <p className="text-secondary small mb-2">
                      Lead Score: <strong className="text-success">{rec.lead_score || 82}</strong> • Deal Stage:{" "}
                      <strong className="text-light">{rec.stage}</strong>
                    </p>

                    <div className="p-3 rounded mb-3 border border-secondary" style={{ backgroundColor: "#0f172a" }}>
                      <div className="fw-semibold text-light small mb-1 d-flex align-items-center">
                        <Zap size={14} className="me-1 text-warning" /> Suggested Action
                      </div>
                      <p className="text-light small mb-0">{rec.recommendation}</p>
                    </div>

                    <p className="text-secondary small mb-3 flex-grow-1">
                      <strong>AI Reason:</strong> {rec.reason}
                    </p>

                    <div className="d-flex justify-content-between align-items-center pt-2 border-top border-secondary mt-auto">
                      <span className="text-muted" style={{ fontSize: "11px" }}>
                        {rec.completed ? (
                          <span className="text-success d-flex align-items-center">
                            <CheckCircle size={14} className="me-1" /> Completed
                          </span>
                        ) : (
                          <span className="text-warning d-flex align-items-center">
                            <Clock size={14} className="me-1" /> Action Pending
                          </span>
                        )}
                      </span>

                      <button
                        onClick={() => handleResolve(rec.id, rec.completed)}
                        className={`btn btn-sm ${
                          rec.completed ? "btn-outline-secondary" : "btn-outline-success"
                        } d-flex align-items-center`}
                      >
                        <Check size={14} className="me-1" />
                        {rec.completed ? "Reopen" : "Mark Resolved"}
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </NextMainLayout>
  );
}
