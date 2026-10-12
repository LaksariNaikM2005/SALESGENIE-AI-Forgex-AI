"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import {
  Users,
  Search,
  Filter,
  Plus,
  RefreshCw,
  ExternalLink,
  Cpu,
  Trash2,
  ChevronLeft,
  ChevronRight,
  Database,
  CheckCircle,
} from "lucide-react";

export default function LeadsPage() {
  const { user, token } = useAuth();
  const router = useRouter();

  const [leads, setLeads] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [perPage] = useState<number>(10);
  const [search, setSearch] = useState<string>("");
  const [sector, setSector] = useState<string>("all");
  const [stage, setStage] = useState<string>("all");
  const [loading, setLoading] = useState<boolean>(true);
  const [syncing, setSyncing] = useState<boolean>(false);
  const [syncMessage, setSyncMessage] = useState<string>("");

  // Create lead modal state
  const [showModal, setShowModal] = useState<boolean>(false);
  const [newCompany, setNewCompany] = useState<string>("");
  const [newContact, setNewContact] = useState<string>("");
  const [newEmail, setNewEmail] = useState<string>("");
  const [newSector, setNewSector] = useState<string>("Industrial Automation");
  const [newValue, setNewValue] = useState<number>(125000);
  const [newTechStack, setNewTechStack] = useState<string>("ROS2, Siemens PLC, Fanuc CNC");

  useEffect(() => {
    fetchLeads();
  }, [page, search, sector, stage]);

  const fetchLeads = async () => {
    setLoading(true);
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const params: any = { page, per_page: perPage };
      if (search.trim()) params.search = search.trim();
      if (sector !== "all") params.sector = sector;
      if (stage !== "all") params.stage = stage;

      const res = await axios.get("/api/leads", { headers, params });
      setLeads(res.data.leads || []);
      setTotal(res.data.total || 0);
    } catch (err) {
      console.error("Error fetching leads:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateLead = async (e: React.FormEvent) => {
    e.preventDefault();
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      await axios.post(
        "/api/leads",
        {
          company: newCompany,
          contact_name: newContact,
          email: newEmail,
          sector: newSector,
          value: newValue,
          tech_stack: newTechStack,
        },
        { headers }
      );
      setShowModal(false);
      setNewCompany("");
      setNewContact("");
      setNewEmail("");
      fetchLeads();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Could not create lead");
    }
  };

  const handleSyncDataset = async () => {
    if (!confirm("Synchronize 5,000 real-world records via Celery background worker?")) return;
    setSyncing(true);
    setSyncMessage("");
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const res = await axios.post("/api/leads/sync-real-dataset", {}, { headers });
      setSyncMessage(res.data.message || "Synchronization completed successfully!");
      fetchLeads();
    } catch (err: any) {
      setSyncMessage(err.response?.data?.detail || "Sync failed. Administrator privileges required.");
    } finally {
      setSyncing(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to remove this lead?")) return;
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      await axios.delete(`/api/leads/${id}`, { headers });
      fetchLeads();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Only Sales Directors and Admins can delete prospects.");
    }
  };

  const totalPages = Math.ceil(total / perPage) || 1;

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        {/* Title Bar */}
        <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
          <div>
            <h1 className="h3 fw-bold text-white mb-1">Manufacturing Lead Intelligence</h1>
            <p className="text-secondary small mb-0">
              Scored with Scikit-learn Machine Learning pipeline & enriched with hardware tech stacks.
            </p>
          </div>

          <div className="d-flex gap-2">
            {user?.role === "admin" && (
              <button
                onClick={handleSyncDataset}
                disabled={syncing}
                className="btn btn-outline-info btn-sm d-flex align-items-center"
              >
                <Database size={15} className={`me-2 ${syncing ? "animate-spin" : ""}`} />
                {syncing ? "Syncing Celery Worker..." : "Sync 5,000 Pipeline Records"}
              </button>
            )}
            <button onClick={() => setShowModal(true)} className="btn btn-primary btn-sm d-flex align-items-center">
              <Plus size={16} className="me-1" /> Add Manufacturing Lead
            </button>
          </div>
        </div>

        {syncMessage && (
          <div className="alert alert-info py-2 small d-flex align-items-center mb-4">
            <CheckCircle size={16} className="me-2 text-info" />
            {syncMessage}
          </div>
        )}

        {/* Filters and Search */}
        <div className="card bg-dark border-secondary p-3 mb-4">
          <div className="row g-2">
            <div className="col-12 col-md-5">
              <div className="input-group input-group-sm">
                <span className="input-group-text bg-secondary border-secondary text-light">
                  <Search size={14} />
                </span>
                <input
                  type="text"
                  className="form-control bg-dark text-white border-secondary"
                  placeholder="Search company, contact, or email..."
                  value={search}
                  onChange={(e) => {
                    setSearch(e.target.value);
                    setPage(1);
                  }}
                />
              </div>
            </div>

            <div className="col-6 col-md-3">
              <select
                className="form-select form-select-sm bg-dark text-white border-secondary"
                value={sector}
                onChange={(e) => {
                  setSector(e.target.value);
                  setPage(1);
                }}
              >
                <option value="all">All Sectors</option>
                <option value="Industrial Automation">Industrial Automation</option>
                <option value="Semiconductor">Semiconductor Fabs</option>
                <option value="Automotive">Automotive Parts</option>
                <option value="CNC">Precision CNC Tooling</option>
                <option value="Heavy Equipment">Heavy Equipment</option>
              </select>
            </div>

            <div className="col-6 col-md-3">
              <select
                className="form-select form-select-sm bg-dark text-white border-secondary"
                value={stage}
                onChange={(e) => {
                  setStage(e.target.value);
                  setPage(1);
                }}
              >
                <option value="all">All Deal Stages</option>
                <option value="New Lead">New Lead</option>
                <option value="Qualified">Qualified</option>
                <option value="Proposal">Proposal</option>
                <option value="Negotiation">Negotiation</option>
                <option value="Won">Closed Won</option>
              </select>
            </div>

            <div className="col-12 col-md-1 d-flex">
              <button
                onClick={() => {
                  setSearch("");
                  setSector("all");
                  setStage("all");
                  setPage(1);
                }}
                className="btn btn-sm btn-outline-secondary w-100"
              >
                Reset
              </button>
            </div>
          </div>
        </div>

        {/* Leads Table */}
        <div className="card bg-dark border-secondary p-0 overflow-hidden mb-3">
          <div className="table-responsive">
            <table className="table table-dark table-hover align-middle mb-0">
              <thead style={{ backgroundColor: "#1e293b" }}>
                <tr className="text-secondary small">
                  <th className="ps-3">Company & Contact</th>
                  <th>Manufacturing Sub-Sector</th>
                  <th>Hardware / Tech Stack</th>
                  <th>Stage</th>
                  <th>Deal Value</th>
                  <th>ML Score</th>
                  <th>Win Prob</th>
                  <th className="text-end pe-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan={8} className="text-center py-5 text-secondary">
                      <div className="spinner-border spinner-border-sm text-primary me-2" />
                      Loading prospects...
                    </td>
                  </tr>
                ) : leads.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="text-center py-5 text-secondary">
                      No leads match current filters.
                    </td>
                  </tr>
                ) : (
                  leads.map((lead: any) => (
                    <tr key={lead.id}>
                      <td className="ps-3">
                        <div className="fw-bold text-white">{lead.company}</div>
                        <div className="text-secondary small">
                          {lead.contact_name} • {lead.email}
                        </div>
                      </td>
                      <td>
                        <span className="badge bg-secondary bg-opacity-50 text-light">{lead.sector}</span>
                      </td>
                      <td>
                        <div className="d-flex flex-wrap gap-1">
                          {(lead.tech_stack || "ROS2, Siemens PLC")
                            .split(",")
                            .map((tech: string, i: number) => (
                              <span
                                key={i}
                                className="badge bg-dark border border-secondary text-info small"
                                style={{ fontSize: "10px" }}
                              >
                                <Cpu size={10} className="me-1 inline" />
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
                        <span className="fw-bold text-success">{lead.lead_score || 75} / 100</span>
                      </td>
                      <td>
                        <span className="text-info fw-semibold">
                          {Math.round((lead.purchase_probability || 0.75) * 100)}%
                        </span>
                      </td>
                      <td className="text-end pe-3">
                        <div className="d-inline-flex gap-1">
                          <button
                            onClick={() => router.push(`/leads/${lead.id}`)}
                            className="btn btn-sm btn-outline-primary py-1 px-2"
                            title="View AI Lead Insights"
                          >
                            <ExternalLink size={14} />
                          </button>
                          {(user?.role === "admin" || user?.role === "sales_manager") && (
                            <button
                              onClick={() => handleDelete(lead.id)}
                              className="btn btn-sm btn-outline-danger py-1 px-2"
                              title="Delete Lead"
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

          {/* Pagination */}
          <div className="d-flex justify-content-between align-items-center p-3 border-top border-secondary">
            <span className="text-secondary small">
              Showing {(page - 1) * perPage + 1} to {Math.min(page * perPage, total)} of {total} prospects
            </span>
            <div className="d-flex gap-2">
              <button
                className="btn btn-sm btn-outline-secondary"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                <ChevronLeft size={16} /> Prev
              </button>
              <span className="px-2 py-1 text-light small fw-bold">
                {page} / {totalPages}
              </span>
              <button
                className="btn btn-sm btn-outline-secondary"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next <ChevronRight size={16} />
              </button>
            </div>
          </div>
        </div>

        {/* Create Lead Modal */}
        {showModal && (
          <div
            className="modal show d-block"
            style={{ backgroundColor: "rgba(0,0,0,0.7)" }}
            tabIndex={-1}
          >
            <div className="modal-dialog modal-dialog-centered">
              <div className="modal-content bg-dark border-secondary text-white">
                <div className="modal-header border-secondary">
                  <h5 className="modal-title fw-bold">Add Manufacturing Prospect</h5>
                  <button
                    type="button"
                    className="btn-close btn-close-white"
                    onClick={() => setShowModal(false)}
                  />
                </div>
                <form onSubmit={handleCreateLead}>
                  <div className="modal-body">
                    <div className="mb-3">
                      <label className="form-label small">Company Account Name *</label>
                      <input
                        type="text"
                        className="form-control bg-dark border-secondary text-white"
                        value={newCompany}
                        onChange={(e) => setNewCompany(e.target.value)}
                        required
                        placeholder="e.g. Apex Precision Robotics"
                      />
                    </div>
                    <div className="row g-2 mb-3">
                      <div className="col-6">
                        <label className="form-label small">Contact Person</label>
                        <input
                          type="text"
                          className="form-control bg-dark border-secondary text-white"
                          value={newContact}
                          onChange={(e) => setNewContact(e.target.value)}
                          placeholder="e.g. Dr. Frank Miller"
                        />
                      </div>
                      <div className="col-6">
                        <label className="form-label small">Contact Email</label>
                        <input
                          type="email"
                          className="form-control bg-dark border-secondary text-white"
                          value={newEmail}
                          onChange={(e) => setNewEmail(e.target.value)}
                          placeholder="frank@apex.com"
                        />
                      </div>
                    </div>
                    <div className="row g-2 mb-3">
                      <div className="col-6">
                        <label className="form-label small">Manufacturing Sub-Sector</label>
                        <select
                          className="form-select bg-dark border-secondary text-white"
                          value={newSector}
                          onChange={(e) => setNewSector(e.target.value)}
                        >
                          <option value="Industrial Automation">Industrial Automation</option>
                          <option value="Semiconductor Fabrication">Semiconductor Fabrication</option>
                          <option value="Automotive Parts">Automotive Parts</option>
                          <option value="Precision CNC Tooling">Precision CNC Tooling</option>
                          <option value="Heavy Equipment">Heavy Equipment</option>
                        </select>
                      </div>
                      <div className="col-6">
                        <label className="form-label small">Estimated Deal Value ($)</label>
                        <input
                          type="number"
                          className="form-control bg-dark border-secondary text-white"
                          value={newValue}
                          onChange={(e) => setNewValue(Number(e.target.value))}
                        />
                      </div>
                    </div>
                    <div className="mb-3">
                      <label className="form-label small">Hardware & Tech Stack</label>
                      <input
                        type="text"
                        className="form-control bg-dark border-secondary text-white"
                        value={newTechStack}
                        onChange={(e) => setNewTechStack(e.target.value)}
                        placeholder="e.g. ROS2, Siemens S7 PLC, Fanuc CNC"
                      />
                    </div>
                  </div>
                  <div className="modal-footer border-secondary">
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() => setShowModal(false)}
                    >
                      Cancel
                    </button>
                    <button type="submit" className="btn btn-primary btn-sm">
                      Create & Run ML Score
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        )}
      </div>
    </NextMainLayout>
  );
}
