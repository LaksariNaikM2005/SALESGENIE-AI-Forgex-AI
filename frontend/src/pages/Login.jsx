import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Zap, Lock, Mail } from 'lucide-react';

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

  return (
    <div className="d-flex align-items-center justify-content-center vh-100" style={{ backgroundColor: '#0f172a' }}>
      <div className="card border-secondary shadow-lg p-4" style={{ width: '420px', backgroundColor: '#1e293b', color: '#f8fafc' }}>
        <div className="text-center mb-4">
          <Zap className="text-primary mb-2" size={48} />
          <h3 className="fw-bold text-white mb-1">SalesGenie AI</h3>
          <p className="small" style={{ color: '#cbd5e1' }}>Sign in to your sales intelligence portal</p>
        </div>

        {error && <div className="alert alert-danger p-2 small text-center mb-3">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Email Address</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><Mail size={16} /></span>
              <input
                type="email"
                className="form-control bg-dark text-light border-secondary"
                placeholder="user@salesgenie.ai"
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
            {loading ? 'Authenticating...' : 'Sign In'}
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
