"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import {
  Calendar,
  CheckCircle,
  Clock,
  Phone,
  Mail,
  Users,
  Check,
  Plus,
} from "lucide-react";

export default function FollowUpsPage() {
  const { token } = useAuth();
  const [followups, setFollowups] = useState<any[]>([]);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchFollowups();
  }, [statusFilter]);

  const fetchFollowups = async () => {
    setLoading(true);
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const params: any = {};
      if (statusFilter !== "all") params.status = statusFilter;

      const res = await axios.get("/api/followups", { headers, params });
      setFollowups(res.data.followups || []);
    } catch (err) {
      console.error("Failed to fetch followups:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (id: number, currentCompleted: boolean) => {
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      await axios.put(`/api/followups/${id}`, { completed: !currentCompleted }, { headers });
      setFollowups((prev) =>
        prev.map((f) =>
          f.id === id ? { ...f, completed: !currentCompleted, status: !currentCompleted ? "Completed" : "Pending" } : f
        )
      );
    } catch (err) {
      console.error("Failed to update followup:", err);
    }
  };

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
          <div>
            <h1 className="h3 fw-bold text-white mb-1">Follow-Up Schedule & Task Pipeline</h1>
            <p className="text-secondary small mb-0">
              Timely touchpoints and planned touchpoints with key manufacturing buyers.
            </p>
          </div>

          <div className="d-flex gap-2">
            {["all", "Pending", "Completed"].map((s) => (
              <button
                key={s}
                onClick={() => setStatusFilter(s)}
                className={`btn btn-sm ${
                  statusFilter === s ? "btn-primary" : "btn-outline-secondary text-secondary"
                }`}
              >
                {s === "all" ? "All Tasks" : s}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center py-5 text-secondary">
            <div className="spinner-border text-primary me-2" /> Loading follow-ups...
          </div>
        ) : followups.length === 0 ? (
          <div className="alert alert-secondary">No scheduled follow-ups found for this filter.</div>
        ) : (
          <div className="card bg-dark border-secondary p-0 overflow-hidden">
            <div className="table-responsive">
              <table className="table table-dark table-hover align-middle mb-0">
                <thead style={{ backgroundColor: "#1e293b" }}>
                  <tr className="text-secondary small">
                    <th className="ps-3">Company & Contact</th>
                    <th>Channel</th>
                    <th>Type</th>
                    <th>Priority</th>
                    <th>Notes</th>
                    <th>Status</th>
                    <th className="text-end pe-3">Action</th>
                  </tr>
                </thead>
                <tbody>
                  {followups.map((f) => (
                    <tr key={f.id}>
                      <td className="ps-3">
                        <div className="fw-bold text-white">{f.lead_company}</div>
                        <div className="text-secondary small">{f.lead_contact}</div>
                      </td>
                      <td>
                        <span className="badge bg-secondary bg-opacity-50 text-light">{f.channel || "Phone"}</span>
                      </td>
                      <td>{f.follow_up_type || "Call"}</td>
                      <td>
                        <span
                          className={`badge ${
                            f.priority === "High" ? "bg-danger" : f.priority === "Medium" ? "bg-warning text-dark" : "bg-info text-dark"
                          }`}
                        >
                          {f.priority || "Medium"}
                        </span>
                      </td>
                      <td className="text-secondary small">{f.notes || "Standard touchpoint"}</td>
                      <td>
                        <span className={`badge ${f.completed ? "bg-success" : "bg-secondary"}`}>
                          {f.completed ? "Completed" : "Pending"}
                        </span>
                      </td>
                      <td className="text-end pe-3">
                        <button
                          onClick={() => handleToggleComplete(f.id, f.completed)}
                          className={`btn btn-sm ${f.completed ? "btn-outline-secondary" : "btn-outline-success"} py-1 px-2`}
                        >
                          <Check size={14} className="me-1" />
                          {f.completed ? "Reopen" : "Done"}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </NextMainLayout>
  );
}
