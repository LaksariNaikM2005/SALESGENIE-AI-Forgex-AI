"use client";

import { FormEvent, useState } from "react";
import { apiRequest } from "@/lib/api";

type Role = "admin" | "sales_manager" | "sales_rep";

type CreatedUser = {
  id: number;
  name: string;
  email: string;
  role: Role;
  is_active: boolean;
};

export default function AdminUsersPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("sales_rep");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function createAccount(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      // Replace this with your established authentication provider or
      // server-side session integration. Never accept a token from a
      // user-editable role field or query parameter.
      const token = sessionStorage.getItem("access_token");

      if (!token) {
        throw new Error("Please sign in again.");
      }

      const user = await apiRequest<CreatedUser>(
        "/api/admin/users",
        token,
        {
          method: "POST",
          body: JSON.stringify({ name, email, password, role }),
        },
      );

      setMessage(`Created ${user.email} as ${user.role}.`);
      setName("");
      setEmail("");
      setPassword("");
      setRole("sales_rep");
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Could not create account.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-bold">Manage SalesGenie AI accounts</h1>
      <p className="mt-2 text-sm text-gray-600">
        Create accounts and assign access levels.
      </p>

      <form onSubmit={createAccount} className="mt-6 space-y-4">
        <label className="block">
          <span className="mb-1 block">Full name</span>
          <input
            className="w-full rounded border p-2"
            value={name}
            onChange={(e) => setName(e.target.value)}
            minLength={2}
            maxLength={120}
            required
          />
        </label>

        <label className="block">
          <span className="mb-1 block">Email</span>
          <input
            className="w-full rounded border p-2"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>

        <label className="block">
          <span className="mb-1 block">Temporary password</span>
          <input
            className="w-full rounded border p-2"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={12}
            maxLength={128}
            autoComplete="new-password"
            required
          />
        </label>

        <label className="block">
          <span className="mb-1 block">Account role</span>
          <select
            className="w-full rounded border p-2"
            value={role}
            onChange={(e) => setRole(e.target.value as Role)}
          >
            <option value="sales_rep">Sales Representative</option>
            <option value="sales_manager">Sales Manager</option>
            <option value="admin">Administrator</option>
          </select>
        </label>

        <button
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
          type="submit"
          disabled={loading}
        >
          {loading ? "Creating..." : "Create account"}
        </button>

        {message && <p role="status">{message}</p>}
      </form>
    </main>
  );
}