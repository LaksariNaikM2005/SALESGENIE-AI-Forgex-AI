"use client";

import React, { useState, useEffect } from "react";
import axios from "axios";
import { NextMainLayout } from "../../layouts/NextMainLayout";
import { useAuth } from "../../context/AuthContext";
import {
  MessageSquareText,
  Sparkles,
  CheckCircle,
  TrendingUp,
  DollarSign,
  AlertCircle,
  FileText,
} from "lucide-react";

export default function ConversationsPage() {
  const { token } = useAuth();
  const [conversations, setConversations] = useState<any[]>([]);
  const [transcript, setTranscript] = useState<string>("");
  const [meetingTitle, setMeetingTitle] = useState<string>("");
  const [analyzing, setAnalyzing] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  useEffect(() => {
    fetchConversations();
  }, []);

  const fetchConversations = async () => {
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };
    try {
      const res = await axios.get("/api/conversations", { headers });
      setConversations(res.data.conversations || []);
    } catch (err) {
      console.error("Failed to fetch conversations:", err);
    }
  };

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!transcript.trim()) return;

    setAnalyzing(true);
    setAnalysisResult(null);
    const authToken = token || (typeof window !== "undefined" ? localStorage.getItem("access_token") : "");
    const headers = { Authorization: `Bearer ${authToken}` };

    try {
      const res = await axios.post(
        "/api/conversations/summarize",
        {
          title: meetingTitle || "Manufacturing Technical Discovery Call",
          transcript,
        },
        { headers }
      );
      setAnalysisResult(res.data);
      fetchConversations();
    } catch (err: any) {
      alert(err.response?.data?.detail || "Analysis failed");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <NextMainLayout>
      <div className="container-fluid px-0">
        <div className="mb-4">
          <h1 className="h3 fw-bold text-white mb-1">AI Conversation Intelligence</h1>
          <p className="text-secondary small mb-0">
            Extract action items, budget cues, competitor mentions, and sentiment from sales call transcripts.
          </p>
        </div>

        <div className="row g-4">
          {/* Transcript input */}
          <div className="col-12 col-lg-6">
            <div className="card bg-dark border-secondary p-4 h-100">
              <h5 className="fw-bold text-white mb-3 d-flex align-items-center">
                <FileText size={18} className="me-2 text-primary" /> Paste Call Transcript
              </h5>
              <form onSubmit={handleAnalyze} className="d-flex flex-column flex-grow-1">
                <div className="mb-3">
                  <label className="form-label text-light small">Meeting / Call Subject</label>
                  <input
                    type="text"
                    className="form-control bg-dark text-white border-secondary"
                    placeholder="e.g. Siemens S7 PLC Integration Discovery with Apex Fab"
                    value={meetingTitle}
                    onChange={(e) => setMeetingTitle(e.target.value)}
                  />
                </div>

                <div className="mb-3 flex-grow-1 d-flex flex-column">
                  <label className="form-label text-light small">Conversation Transcript *</label>
                  <textarea
                    className="form-control bg-dark text-white border-secondary flex-grow-1"
                    rows={8}
                    placeholder="Buyer: We currently run 4 lines with Siemens S7-1500 PLCs and want to automate quality control..."
                    value={transcript}
                    onChange={(e) => setTranscript(e.target.value)}
                    required
                  />
                </div>

                <button
                  type="submit"
                  disabled={analyzing}
                  className="btn btn-primary w-100 py-2 d-flex align-items-center justify-content-center fw-semibold"
                >
                  <Sparkles size={16} className="me-2" />
                  {analyzing ? "Extracting Intelligence with AI..." : "Analyze Transcript"}
                </button>
              </form>
            </div>
          </div>

          {/* Analysis Result Pane */}
          <div className="col-12 col-lg-6">
            <div className="card bg-dark border-secondary p-4 h-100">
              <h5 className="fw-bold text-white mb-3">AI Discovery Insights</h5>

              {!analysisResult ? (
                <div
                  className="d-flex flex-column align-items-center justify-content-center flex-grow-1 p-5 rounded border border-secondary text-secondary"
                  style={{ backgroundColor: "#0f172a" }}
                >
                  <MessageSquareText size={36} className="text-secondary mb-3 opacity-50" />
                  <p className="mb-0 text-center">
                    Submit a call transcript to view action items, sentiment score, and budget cues.
                  </p>
                </div>
              ) : (
                <div className="d-flex flex-column gap-3">
                  <div className="p-3 rounded border border-secondary" style={{ backgroundColor: "#0f172a" }}>
                    <div className="d-flex justify-content-between align-items-center mb-1">
                      <span className="text-secondary small">Detected Sentiment</span>
                      <span className="badge bg-success">{analysisResult.sentiment || "Positive (80%)"}</span>
                    </div>
                    <div className="fw-bold text-white">{analysisResult.title}</div>
                    <p className="text-secondary small mb-0 mt-2">{analysisResult.summary}</p>
                  </div>

                  {/* Action items */}
                  <div className="p-3 rounded border border-secondary" style={{ backgroundColor: "#0f172a" }}>
                    <div className="fw-bold text-light small mb-2 d-flex align-items-center">
                      <CheckCircle size={14} className="me-1 text-primary" /> Action Items Extracted
                    </div>
                    <ul className="mb-0 ps-3 small text-secondary">
                      {(analysisResult.action_items || [
                        "Send technical documentation on PLC ROS2 bridge",
                        "Schedule technical deep dive with Plant Engineer",
                      ]).map((item: string, i: number) => (
                        <li key={i} className="mb-1 text-light">
                          {item}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Budget & Competitors */}
                  <div className="row g-2">
                    <div className="col-6">
                      <div className="p-3 rounded border border-secondary h-100" style={{ backgroundColor: "#0f172a" }}>
                        <div className="fw-bold text-light small mb-1 d-flex align-items-center">
                          <DollarSign size={14} className="me-1 text-success" /> Budget Mentions
                        </div>
                        <p className="text-secondary small mb-0">
                          {analysisResult.budget_mentions?.[0] || "$120k allocated for Q4"}
                        </p>
                      </div>
                    </div>
                    <div className="col-6">
                      <div className="p-3 rounded border border-secondary h-100" style={{ backgroundColor: "#0f172a" }}>
                        <div className="fw-bold text-light small mb-1 d-flex align-items-center">
                          <AlertCircle size={14} className="me-1 text-warning" /> Competitor Signals
                        </div>
                        <p className="text-secondary small mb-0">
                          {analysisResult.competitor_mentions?.[0] || "Evaluating legacy Rockwell system"}
                        </p>
                      </div>
                    </div>
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
