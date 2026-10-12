import React from "react";
import type { Metadata } from "next";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import "../index.css";
import { AuthProvider } from "../context/AuthContext";

export const metadata: Metadata = {
  title: "SalesGenie AI — B2B Manufacturing Sales Intelligence",
  description:
    "Next.js + FastAPI + PostgreSQL + Redis + Celery Enterprise Sales Intelligence and Prospect Qualification Engine",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-bs-theme="dark">
      <body style={{ backgroundColor: "#0f172a", color: "#f8fafc", margin: 0, padding: 0 }}>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
