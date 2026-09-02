import React, { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { Zap, Lock, Mail, User as UserIcon, CheckCircle, ShieldCheck } from 'lucide-react';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('sales_rep'); // Requirement 8: Role Section
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    setLoading(true);
    try {
      await register(name, email, password, confirmPassword, role);
      setSuccess('Account created successfully! Redirecting to login...');
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.message || err.message || 'Failed to create account');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center vh-100" style={{ backgroundColor: '#0f172a' }}>
      <div className="card border-secondary shadow-lg p-4" style={{ width: '480px', backgroundColor: '#1e293b', color: '#f8fafc' }}>
        <div className="text-center mb-4">
          <Zap className="text-primary mb-2" size={48} />
          <h3 className="fw-bold text-white mb-1">Create Account</h3>
          <p className="small" style={{ color: '#cbd5e1' }}>Join SalesGenie AI Manufacturing Intelligence Platform</p>
        </div>

        {error && <div className="alert alert-danger p-2 small text-center">{error}</div>}
        {success && <div className="alert alert-success p-2 small text-center d-flex align-items-center justify-content-center gap-2"><CheckCircle size={16} />{success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Full Name</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><UserIcon size={16} /></span>
              <input
                type="text"
                className="form-control bg-dark text-light border-secondary"
                placeholder="e.g. Alex Morgan"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-3">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Email Address</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><Mail size={16} /></span>
              <input
                type="email"
                className="form-control bg-dark text-light border-secondary"
                placeholder="alex@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          {/* Requirement 8: Role Section in User Registration */}
          <div className="mb-3">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Select Company Role *</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary text-warning"><ShieldCheck size={16} /></span>
              <select
                className="form-select bg-dark text-light border-secondary fw-semibold"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                required
              >
                <option value="sales_rep">Sales Representative (Account Executive)</option>
                <option value="sales_manager">Sales Director / Manager</option>
                <option value="admin">System Administrator</option>
              </select>
            </div>
          </div>

          <div className="mb-3">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><Lock size={16} /></span>
              <input
                type="password"
                className="form-control bg-dark text-light border-secondary"
                placeholder="Min 8 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label small fw-medium" style={{ color: '#e2e8f0' }}>Confirm Password</label>
            <div className="input-group">
              <span className="input-group-text bg-dark border-secondary" style={{ color: '#94a3b8' }}><Lock size={16} /></span>
              <input
                type="password"
                className="form-control bg-dark text-light border-secondary"
                placeholder="Re-enter password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary w-100 py-2 fw-semibold" disabled={loading}>
            {loading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <div className="text-center mt-3 pt-3 border-top border-secondary">
          <span className="small" style={{ color: '#cbd5e1' }}>Already have an account? </span>
          <Link to="/login" className="text-primary small text-decoration-none fw-semibold">Sign In</Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
