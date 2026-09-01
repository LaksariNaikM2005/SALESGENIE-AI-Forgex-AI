import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Zap, Lock, Mail } from 'lucide-react';

const Login = () => {
  const [email, setEmail] = useState('admin@salesgenie.ai');
  const [password, setPassword] = useState('AdminPass123!');
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
      setError(err.response?.data?.error || 'Invalid credentials or backend unreachable');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100" style={{ backgroundColor: '#0f172a' }}>
      <div className="card border-secondary shadow-lg p-4" style={{ width: '400px', backgroundColor: '#1e293b', color: '#f8fafc' }}>
        <div className="text-center mb-4">
          <Zap className="text-primary mb-2" size={48} />
          <h3 className="fw-bold">SalesGenie AI</h3>
          <p className="text-muted small">Sign in to your sales intelligence portal</p>
        </div>
        {error && <div className="alert alert-danger p-2 small text-center">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label small text-muted">Email Address</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-muted"><Mail size={16} /></span>
              <input
                type="email"
                className="form-control bg-dark text-light border-secondary"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="mb-4">
            <label className="form-label small text-muted">Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-muted"><Lock size={16} /></span>
              <input
                type="password"
                className="form-control bg-dark text-light border-secondary"
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
      </div>
    </div>
  );
};

export default Login;
