import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Zap, Lock, Mail, ShieldCheck, Users, Award } from 'lucide-react';

const DEMO_ACCOUNTS = [
  { label: 'Admin', email: 'admin@forgex.ai', password: 'Admin@123', color: 'danger', icon: <ShieldCheck size={13} /> },
  { label: 'Manager', email: 'manager@forgex.ai', password: 'Manager@123', color: 'warning', icon: <Award size={13} /> },
  { label: 'Sales Rep', email: 'sales@forgex.ai', password: 'Sales@123', color: 'info', icon: <Users size={13} /> },
];

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(email, password);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.message || err.message || 'Invalid credentials or backend unreachable');
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (demo) => {
    setEmail(demo.email);
    setPassword(demo.password);
    setError('');
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100" style={{ backgroundColor: '#0f172a' }}>
      <div className="card border-secondary shadow-lg p-4" style={{ width: '440px', backgroundColor: '#1e293b', color: '#f8fafc' }}>
        {/* Header */}
        <div className="text-center mb-4">
          <div className="d-flex align-items-center justify-content-center gap-2 mb-2">
            <Zap className="text-primary" size={36} />
            <h3 className="fw-bold text-white mb-0">FORGE_X AI</h3>
          </div>
          <p className="small mb-0" style={{ color: '#94a3b8' }}>
            SalesGenie AI — Manufacturing Intelligence Platform
          </p>
          <p className="small mt-1" style={{ color: '#64748b' }}>Sign in to your sales intelligence portal</p>
        </div>

        {error && <div className="alert alert-danger p-2 small text-center mb-3">{error}</div>}

        {/* Demo Accounts */}
        <div className="mb-3 p-3 rounded border border-secondary" style={{ backgroundColor: '#0f172a' }}>
          <p className="small fw-semibold text-muted mb-2">🔐 Demo Accounts (click to fill):</p>
          <div className="d-flex gap-2 flex-wrap">
            {DEMO_ACCOUNTS.map(demo => (
              <button
                key={demo.label}
                type="button"
                className={`btn btn-outline-${demo.color} btn-sm d-flex align-items-center gap-1`}
                onClick={() => fillDemo(demo)}
              >
                {demo.icon} {demo.label}
              </button>
            ))}
          </div>
          <p className="small mt-2 mb-0" style={{ color: '#64748b' }}>
            Admin: Full access | Manager: Team view | Sales Rep: Standard access
          </p>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Email Address</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><Mail size={16} /></span>
              <input
                type="email"
                className="form-control bg-dark text-light border-secondary"
                placeholder="user@forgex.ai"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><Lock size={16} /></span>
              <input
                type="password"
                className="form-control bg-dark text-light border-secondary"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary w-100 py-2 fw-semibold" disabled={loading}>
            {loading ? (
              <><span className="spinner-border spinner-border-sm me-2" /> Authenticating...</>
            ) : (
              'Sign In to FORGE_X AI'
            )}
          </button>
        </form>

        <div className="text-center mt-3 pt-3 border-top border-secondary">
          <span className="small" style={{ color: '#cbd5e1' }}>Don't have an account? </span>
          <Link to="/register" className="text-primary small text-decoration-none fw-semibold">Create Account</Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
