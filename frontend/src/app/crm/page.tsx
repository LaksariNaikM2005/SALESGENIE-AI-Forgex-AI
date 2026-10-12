"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import { RefreshCw, CheckCircle, Database, Server, ArrowRight } from "lucide-react";

export default function CRMSyncPage() {
  const { token } = useAuth();
  const [connections, setConnections] = useState<any[]>([]);
  const [syncing, setSyncing] = useState<boolean>(false);
  const [syncMsg, setSyncMsg] = useState<string>("");

  useEffect(() => {
    fetchCRMStatus();
  }, []);

  const fetchCRMStatus = async () => {
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };
    try {
      const res = await axios.get("/api/crm/status", { headers });
      setConnections(res.data || []);
    } catch (err) {
      console.error("CRM status error:", err);
    }
  };

  const handleSync = async (provider: string = "all") => {
    setSyncing(true);
    setSyncMsg("");
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const res = await axios.post("/api/crm/sync", { provider }, { headers });
      setSyncMsg(res.data.message || "Bi-directional CRM sync completed successfully!");
      fetchCRMStatus();
    } catch (err) {
      console.error("CRM sync failed:", err);
    } finally {
      setSyncing(false);
    }
  };

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        <div className="d-flex flex-wrap justify-content-between align-items-center mb-4 gap-3">
          <div>
            <h1 className="h3 fw-bold text-white mb-1">CRM Integrations & Bi-Directional Sync</h1>
            <p className="text-secondary small mb-0">
              Synchronize industrial accounts, contacts, and deal stages with Salesforce and HubSpot.
            </p>
          </div>

          <button
            onClick={() => handleSync("all")}
            disabled={syncing}
            className="btn btn-primary btn-sm d-flex align-items-center"
          >
            <RefreshCw size={15} className={`me-2 ${syncing ? "animate-spin" : ""}`} />
            {syncing ? "Synchronizing CRM..." : "Sync All Integrations"}
          </button>
        </div>

        {syncMsg && (
          <div className="alert alert-success py-2 small d-flex align-items-center mb-4">
            <CheckCircle size={16} className="me-2 text-success" /> {syncMsg}
          </div>
        )}

        <div className="row g-4">
          {connections.map((c: any) => (
            <div key={c.id} className="col-12 col-md-6">
              <div className="card bg-dark border-secondary p-4 h-100">
                <div className="d-flex justify-content-between align-items-start mb-3">
                  <div>
                    <h5 className="fw-bold text-white mb-1 text-capitalize">{c.provider}</h5>
                    <div className="text-secondary small">{c.account_name}</div>
                  </div>
                  <span className="badge bg-success">{c.sync_status || "Connected"}</span>
                </div>

                <div className="p-3 rounded mb-3 border border-secondary" style={{ backgroundColor: "#0f172a" }}>
                  <div className="d-flex justify-content-between align-items-center mb-1">
                    <span className="text-secondary small">Last Successful Sync</span>
                    <span className="text-light small fw-semibold">
                      {c.last_sync_at ? new Date(c.last_sync_at).toLocaleString() : "Just now"}
                    </span>
                  </div>
                  <div className="d-flex justify-content-between align-items-center">
                    <span className="text-secondary small">Protocol</span>
                    <span className="text-info small fw-semibold">REST API • OAuth2</span>
                  </div>
                </div>

                <button
                  onClick={() => handleSync(c.provider)}
                  disabled={syncing}
                  className="btn btn-outline-primary btn-sm w-100 mt-auto d-flex align-items-center justify-content-center"
                >
                  <RefreshCw size={14} className="me-1" /> Trigger {c.provider} Sync
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </NextMainLayout>
  );
}
