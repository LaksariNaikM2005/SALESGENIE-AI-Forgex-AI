"use client";

import React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "../context/AuthContext";
import {
  LayoutDashboard,
  Users,
  Sparkles,
  MessageSquareText,
  RefreshCw,
  LogOut,
  Zap,
  User as UserIcon,
  Calendar,
  Lightbulb,
  ShieldCheck,
  Server,
} from "lucide-react";

export const NextMainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/login");
  };

  const role = user?.role || "sales_rep";
  const roleLabel =
    role === "admin"
      ? "System Administrator"
      : role === "sales_manager"
      ? "Sales Director / Manager"
      : "Sales Representative";
  const roleBadgeColor =
    role === "admin"
      ? "bg-danger"
      : role === "sales_manager"
      ? "bg-warning text-dark"
      : "bg-info text-dark";

  const navItems = [
    { label: "Dashboard", path: "/", icon: LayoutDashboard },
    { label: "Lead Intelligence", path: "/leads", icon: Users },
    { label: "AI Recommendations", path: "/recommendations", icon: Lightbulb },
    { label: "Follow-ups", path: "/followups", icon: Calendar },
    { label: "AI Outreach", path: "/outreach", icon: Sparkles },
    { label: "Conversation AI", path: "/conversations", icon: MessageSquareText },
    { label: "CRM Sync", path: "/crm", icon: RefreshCw },
    { label: "Admin Users", path: "/admin/users", icon: ShieldCheck, adminOnly: true },
    { label: "Profile & Settings", path: "/profile", icon: UserIcon },
  ];

  return (
    <div className="d-flex w-100" style={{ minHeight: "100vh", backgroundColor: "#0f172a", color: "#f8fafc" }}>
      {/* Sidebar */}
      <aside
        className="d-flex flex-column p-3 text-white border-end border-secondary flex-shrink-0"
        style={{ width: "260px", backgroundColor: "#1e293b", minHeight: "100vh" }}
      >
        <Link href="/" className="d-flex align-items-center mb-4 text-white text-decoration-none px-2">
          <Zap className="me-2 text-primary" size={28} />
          <div>
            <div className="fs-5 fw-bold tracking-wide">SalesGenie AI</div>
            <div className="text-muted" style={{ fontSize: "11px" }}>Next.js + FastAPI + Postgres</div>
          </div>
        </Link>
        <hr className="bg-secondary mb-3" />

        <ul className="nav nav-pills flex-column mb-auto">
          {navItems.map((item) => {
            if (item.adminOnly && role !== "admin") return null;
            const Icon = item.icon;
            const isActive = pathname === item.path;
            return (
              <li key={item.path} className="nav-item mb-1">
                <Link
                  href={item.path}
                  className={`nav-link d-flex align-items-center px-3 py-2 rounded text-decoration-none ${
                    isActive ? "active bg-primary text-white fw-semibold" : "text-light"
                  }`}
                  style={{
                    backgroundColor: isActive ? "#2563eb" : "transparent",
                    color: isActive ? "#fff" : "#cbd5e1",
                    transition: "all 0.15s ease-in-out",
                  }}
                >
                  <Icon className="me-3" size={18} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>

        {/* Tech Stack Indicator */}
        <div className="p-2 mb-3 rounded" style={{ backgroundColor: "#0f172a", fontSize: "11px" }}>
          <div className="text-muted fw-bold mb-1 d-flex align-items-center">
            <Server size={12} className="me-1 text-success" /> Production Stack
          </div>
          <div className="text-secondary">FastAPI • PostgreSQL • Redis • Celery</div>
        </div>

        <hr className="bg-secondary mb-3" />

        {/* User Card & Logout */}
        <div className="d-flex flex-column gap-2 px-2">
          {user ? (
            <>
              <div className="d-flex flex-column">
                <span className="fw-bold text-truncate" style={{ fontSize: "14px" }}>
                  {user.name}
                </span>
                <span className="text-muted text-truncate" style={{ fontSize: "12px" }}>
                  {user.email}
                </span>
                <span className={`badge ${roleBadgeColor} mt-1 align-self-start`} style={{ fontSize: "10px" }}>
                  {roleLabel}
                </span>
              </div>
              <button
                onClick={handleLogout}
                className="btn btn-sm btn-outline-danger d-flex align-items-center justify-content-center mt-2"
              >
                <LogOut size={14} className="me-2" /> Sign Out
              </button>
            </>
          ) : (
            <Link href="/login" className="btn btn-sm btn-primary w-100">
              Sign In
            </Link>
          )}
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-grow-1 p-4" style={{ backgroundColor: "#0f172a", minHeight: "100vh", overflowY: "auto" }}>
        {children}
      </main>
    </div>
  );
};
