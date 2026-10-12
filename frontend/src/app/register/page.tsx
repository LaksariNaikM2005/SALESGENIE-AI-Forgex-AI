"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import axios from "axios";
import { Zap, Lock, Mail, User, ArrowRight } from "lucide-react";

export default function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      await axios.post("/api/auth/register", {
        name,
        email,
        password,
        confirm_password: confirmPassword,
      });
      setSuccess("Account registered successfully! Redirecting to login...");
      setTimeout(() => router.push("/login"), 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.response?.data?.error || "Registration failed");
    } finally {
      setLoading(false);
    }
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
          <h2 className="fw-bold text-white mb-1">Create Account</h2>
          <p className="text-secondary small">Join SalesGenie AI Manufacturing Sales Platform</p>
        </div>

        {error && <div className="alert alert-danger py-2 small">{error}</div>}
        {success && <div className="alert alert-success py-2 small">{success}</div>}

        <form onSubmit={handleRegister}>
          <div className="mb-3">
            <label className="form-label text-light small fw-semibold">Full Name</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary">
                <User size={16} />
              </span>
              <input
                type="text"
                className="form-control bg-dark text-white border-secondary"
                placeholder="Marcus Vance"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-3">
            <label className="form-label text-light small fw-semibold">Work Email</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary">
                <Mail size={16} />
              </span>
              <input
                type="email"
                className="form-control bg-dark text-white border-secondary"
                placeholder="marcus@manufacturing.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-3">
            <label className="form-label text-light small fw-semibold">Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary">
                <Lock size={16} />
              </span>
              <input
                type="password"
                className="form-control bg-dark text-white border-secondary"
                placeholder="At least 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label text-light small fw-semibold">Confirm Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-secondary">
                <Lock size={16} />
              </span>
              <input
                type="password"
                className="form-control bg-dark text-white border-secondary"
                placeholder="Re-enter password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary w-100 py-2 fw-semibold d-flex align-items-center justify-content-center" disabled={loading}>
            {loading ? "Registering..." : <>Create Account <ArrowRight size={16} className="ms-2" /></>}
          </button>
        </form>

        <div className="text-center mt-3">
          <span className="text-secondary small">Already have an account? </span>
          <Link href="/login" className="small text-primary text-decoration-none fw-semibold">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
