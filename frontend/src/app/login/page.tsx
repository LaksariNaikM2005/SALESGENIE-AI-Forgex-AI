"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "../../context/AuthContext";
import { Zap, Lock, Mail, ShieldCheck, ArrowRight, UserCheck } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    const success = await login(email, password);
    setLoading(false);

    if (success) {
      router.push("/");
    } else {
      setError("Invalid email or password. Please verify credentials.");
    }
  };

  const setDemoCredentials = (roleEmail: string, rolePass: string) => {
    setEmail(roleEmail);
    setPassword(rolePass);
  };

  return (
    <div
      className="d-flex align-items-center justify-content-center w-100 min-vh-100"
      style={{
        backgroundColor: "#0f172a",
        backgroundImage: "radial-gradient(#1e293b 1px, transparent 1px)",
        backgroundSize: "24px 24px",
      }}
    >
      <div className="card border-secondary shadow-lg p-4" style={{ maxWidth: "460px", width: "100%", backgroundColor: "#1e293b" }}>
        <div className="text-center mb-4">
          <div className="d-inline-flex p-3 rounded-circle bg-primary bg-opacity-25 mb-3 text-primary">
            <Zap size={36} />
          </div>
          <h2 className="fw-bold text-white mb-1">SalesGenie AI</h2>
          <p className="text-secondary small">Next.js & FastAPI Manufacturing Sales Intelligence</p>
        </div>

        {error && <div className="alert alert-danger py-2 small">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label text-light small fw-semibold">Work Email</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary">
                <Mail size={16} />
              </span>
              <input
                type="email"
                className="form-control bg-dark text-white border-secondary"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label text-light small fw-semibold">Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary">
                <Lock size={16} />
              </span>
              <input
                type="password"
                className="form-control bg-dark text-white border-secondary"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary w-100 py-2 fw-semibold d-flex align-items-center justify-content-center" disabled={loading}>
            {loading ? "Authenticating with FastAPI..." : <>Sign In <ArrowRight size={16} className="ms-2" /></>}
          </button>
        </form>

        {/* Demo Roles Quick-Fill */}
        <div className="mt-4 pt-3 border-top border-secondary">
          <div className="text-secondary small fw-semibold mb-2 text-center d-flex align-items-center justify-content-center">
            <ShieldCheck size={14} className="me-1 text-info" /> Quick Demo Role Logins
          </div>
          <div className="d-flex flex-column gap-2">
            <button
              type="button"
              className="btn btn-sm btn-outline-danger text-start d-flex justify-content-between align-items-center"
              onClick={() => setDemoCredentials("admin@salesgenie.ai", "AdminPass123!")}
            >
              <span>👑 System Admin</span>
              <span className="badge bg-danger">admin@salesgenie.ai</span>
            </button>
            <button
              type="button"
              className="btn btn-sm btn-outline-warning text-start d-flex justify-content-between align-items-center"
              onClick={() => setDemoCredentials("manager@salesgenie.ai", "ManagerPass123!")}
            >
              <span>👔 Sales Manager</span>
              <span className="badge bg-warning text-dark">manager@salesgenie.ai</span>
            </button>
            <button
              type="button"
              className="btn btn-sm btn-outline-info text-start d-flex justify-content-between align-items-center"
              onClick={() => setDemoCredentials("rep@salesgenie.ai", "RepPass123!")}
            >
              <span>💼 Sales Rep</span>
              <span className="badge bg-info text-dark">rep@salesgenie.ai</span>
            </button>
          </div>
        </div>

        <div className="text-center mt-3">
          <span className="text-secondary small">Need a new account? </span>
          <Link href="/register" className="small text-primary text-decoration-none fw-semibold">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
}
