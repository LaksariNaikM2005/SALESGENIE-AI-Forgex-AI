"use client";

import React, { useEffect, useState } from "react";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import {
  Sparkles,
  Send,
  Copy,
  Check,
  Mail,
  Share2,
  Phone,
  FileText,
  Building,
  Target,
  Sliders,
} from "lucide-react";

export default function OutreachPage() {
  const { token } = useAuth();
  const [leads, setLeads] = useState<any[]>([]);
  const [selectedLead, setSelectedLead] = useState<any>(null);

  // 4 Steps Parameters
  const [channel, setChannel] = useState<string>("Executive Email");
  const [tone, setTone] = useState<string>("Executive & Consultative");
  const [valueProp, setValueProp] = useState<string>("PLC & SCADA Integration");

  // Output
  const [subject, setSubject] = useState<string>("");
  const [body, setBody] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);
  const [sendSuccess, setSendSuccess] = useState<string>("");

  useEffect(() => {
    fetchLeadsList();
  }, []);

  const fetchLeadsList = async () => {
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };
    try {
      const res = await axios.get("/api/leads?per_page=20", { headers });
      const items = res.data.leads || [];
      setLeads(items);
      if (items.length > 0) {
        setSelectedLead(items[0]);
      }
    } catch (err) {
      console.error("Failed to fetch leads for outreach:", err);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    setSendSuccess("");
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const res = await axios.post(
        "/api/outreach/generate",
        {
          lead_name: selectedLead?.contact_name || "Prospect",
          company_name: selectedLead?.company || "Manufacturing Enterprise",
          industry: selectedLead?.sector || "Industrial Automation",
          message_type: channel,
          tone: tone,
          value_prop: valueProp,
          tech_stack: selectedLead?.tech_stack || "Siemens PLC, ROS2",
        },
        { headers }
      );

      setSubject(res.data.subject || "");
      setBody(res.data.body || "");
    } catch (err) {
      console.error("Generation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    const fullText = `${subject ? `Subject: ${subject}\n\n` : ""}${body}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSend = async () => {
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      await axios.post(
        "/api/outreach/send",
        {
          recipient: selectedLead?.email || "decisionmaker@company.com",
          subject,
          body,
        },
        { headers }
      );
      setSendSuccess(`Message successfully dispatched to ${selectedLead?.email || "recipient"}`);
    } catch (err) {
      console.error("Send failed:", err);
    }
  };

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        <div className="mb-4">
          <h1 className="h3 fw-bold text-white mb-1">AI Personalized Outreach Generator</h1>
          <p className="text-secondary small mb-0">
            4-step structured manufacturing messaging tuned for industrial hardware decision-makers.
          </p>
        </div>

        {sendSuccess && (
          <div className="alert alert-success py-2 small mb-4">{sendSuccess}</div>
        )}

        <div className="row g-4">
          {/* Left Column: 4-Step Builder */}
          <div className="col-12 col-lg-5">
            <div className="card bg-dark border-secondary p-4 h-100">
              <h5 className="fw-bold text-white mb-3 d-flex align-items-center">
                <Sliders size={18} className="me-2 text-primary" /> Outreach Configuration
              </h5>

              {/* Step 1: Prospect */}
              <div className="mb-3">
                <label className="form-label text-light small fw-semibold">
                  1. Target Manufacturing Prospect
                </label>
                <select
                  className="form-select form-select-sm bg-dark text-white border-secondary"
                  value={selectedLead?.id || ""}
                  onChange={(e) => {
                    const l = leads.find((item) => item.id === Number(e.target.value));
                    setSelectedLead(l);
                  }}
                >
                  {leads.map((l) => (
                    <option key={l.id} value={l.id}>
                      {l.company} ({l.sector}) — {l.contact_name}
                    </option>
                  ))}
                </select>
                {selectedLead && (
                  <div className="text-secondary small mt-1">
                    Tech Stack: <span className="text-info">{selectedLead.tech_stack || "ROS2, Siemens PLC"}</span>
                  </div>
                )}
              </div>

              {/* Step 2: Channel */}
              <div className="mb-3">
                <label className="form-label text-light small fw-semibold">2. Campaign Channel</label>
                <div className="d-flex flex-wrap gap-2">
                  {[
                    { name: "Executive Email", icon: Mail },
                    { name: "LinkedIn Pitch", icon: Share2 },
                    { name: "Phone Script", icon: Phone },
                    { name: "Commercial Proposal", icon: FileText },
                  ].map((ch) => {
                    const Icon = ch.icon;
                    return (
                      <button
                        key={ch.name}
                        type="button"
                        onClick={() => setChannel(ch.name)}
                        className={`btn btn-sm d-flex align-items-center ${
                          channel === ch.name ? "btn-primary" : "btn-outline-secondary text-secondary"
                        }`}
                      >
                        <Icon size={14} className="me-1" /> {ch.name}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Step 3: Tone */}
              <div className="mb-3">
                <label className="form-label text-light small fw-semibold">
                  3. Tone & Perspective
                </label>
                <select
                  className="form-select form-select-sm bg-dark text-white border-secondary"
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                >
                  <option value="Executive & Consultative">Executive & Consultative</option>
                  <option value="Technical Heavy">Technical Heavy (PLC & Architecture)</option>
                  <option value="Commercial ROI">Commercial ROI & Cost Payback</option>
                  <option value="Urgent Q4">Urgent Q4 Capacity Expansion</option>
                </select>
              </div>

              {/* Step 4: Value Prop */}
              <div className="mb-4">
                <label className="form-label text-light small fw-semibold">
                  4. Primary Value Proposition Focus
                </label>
                <select
                  className="form-select form-select-sm bg-dark text-white border-secondary"
                  value={valueProp}
                  onChange={(e) => setValueProp(e.target.value)}
                >
                  <option value="PLC & SCADA Integration">PLC & SCADA Integration</option>
                  <option value="Line Throughput & Cycle Time">Line Throughput & Cycle Time (-30%)</option>
                  <option value="Zero Defect Quality Control">Zero Defect Automated QC</option>
                  <option value="Enterprise Volume Pricing">Enterprise Volume Pricing & Support</option>
                </select>
              </div>

              <button
                onClick={handleGenerate}
                disabled={loading}
                className="btn btn-primary w-100 py-2 d-flex align-items-center justify-content-center fw-semibold mt-auto"
              >
                <Sparkles size={16} className="me-2" />
                {loading ? "Synthesizing AI Message..." : "Generate AI Outreach"}
              </button>
            </div>
          </div>

          {/* Right Column: Preview Pane */}
          <div className="col-12 col-lg-7">
            <div className="card bg-dark border-secondary p-4 h-100 d-flex flex-column">
              <div className="d-flex justify-content-between align-items-center mb-3">
                <h5 className="fw-bold text-white mb-0">Generated Outreach Preview</h5>
                <div className="d-flex gap-2">
                  <button
                    onClick={handleCopy}
                    disabled={!body}
                    className="btn btn-sm btn-outline-secondary d-flex align-items-center text-light"
                  >
                    {copied ? <Check size={14} className="me-1 text-success" /> : <Copy size={14} className="me-1" />}
                    {copied ? "Copied" : "Copy"}
                  </button>

                  <button
                    onClick={handleSend}
                    disabled={!body}
                    className="btn btn-sm btn-success d-flex align-items-center"
                  >
                    <Send size={14} className="me-1" /> Send Message
                  </button>
                </div>
              </div>

              {!body ? (
                <div
                  className="d-flex flex-column align-items-center justify-content-center flex-grow-1 p-5 rounded border border-secondary text-secondary"
                  style={{ backgroundColor: "#0f172a" }}
                >
                  <Sparkles size={36} className="text-secondary mb-3 opacity-50" />
                  <p className="mb-0 text-center">
                    Select a prospect and click <strong>Generate AI Outreach</strong> to synthesize personalized copy.
                  </p>
                </div>
              ) : (
                <div className="flex-grow-1 d-flex flex-column gap-3">
                  {subject && (
                    <div className="p-3 rounded border border-secondary" style={{ backgroundColor: "#0f172a" }}>
                      <div className="text-secondary small mb-1 fw-semibold">Subject Line:</div>
                      <div className="fw-bold text-white">{subject}</div>
                    </div>
                  )}

                  <div
                    className="p-3 rounded border border-secondary flex-grow-1 text-white"
                    style={{ backgroundColor: "#0f172a", whiteSpace: "pre-wrap", lineHeight: 1.6 }}
                  >
                    {body}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </NextMainLayout>
  );
}
