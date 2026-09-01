import React, { useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import { LayoutDashboard, Users, Sparkles, MessageSquareText, RefreshCw, LogOut, Zap } from 'lucide-react';

const MainLayout = ({ children }) => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { label: 'Dashboard', path: '/', icon: LayoutDashboard },
    { label: 'Lead Intelligence', path: '/leads', icon: Users },
    { label: 'AI Outreach', path: '/outreach', icon: Sparkles },
    { label: 'Conversation AI', path: '/conversations', icon: MessageSquareText },
    { label: 'CRM Sync', path: '/crm', icon: RefreshCw },
  ];

  return (
    <div className="d-flex" style={{ minHeight: '100vh', backgroundColor: '#0f172a', color: '#f8fafc' }}>
      {/* Sidebar */}
      <div className="d-flex flex-column p-3 text-white border-end border-secondary" style={{ width: '260px', backgroundColor: '#1e293b' }}>
        <Link to="/" className="d-flex align-items-center mb-4 text-white text-decoration-none px-2">
          <Zap className="me-2 text-primary" size={28} />
          <span className="fs-4 fw-bold tracking-wide">SalesGenie AI</span>
        </Link>
        <hr className="bg-secondary" />
        <ul className="nav nav-pills flex-column mb-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <li key={item.path} className="nav-item mb-1">
                <Link
                  to={item.path}
                  className={`nav-link d-flex align-items-center px-3 py-2 rounded ${
                    isActive ? 'active bg-primary text-white fw-semibold' : 'text-slate-300 text-decoration-none'
                  }`}
                  style={{ transition: 'all 0.2s' }}
                >
                  <Icon className="me-3" size={20} />
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
        <hr className="bg-secondary" />
        <div className="d-flex align-items-center justify-content-between px-2">
          <div className="d-flex flex-column">
            <span className="fw-semibold text-truncate" style={{ maxWidth: '140px' }}>{user?.name || 'Sales Rep'}</span>
            <small className="text-muted">{user?.role || 'admin'}</small>
          </div>
          <button onClick={handleLogout} className="btn btn-outline-danger btn-sm p-2" title="Logout">
            <LogOut size={16} />
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-grow-1 d-flex flex-column overflow-auto">
        <header className="navbar navbar-expand border-bottom border-secondary px-4 py-3" style={{ backgroundColor: '#1e293b' }}>
          <span className="navbar-brand text-light fw-medium">AI Sales Assistant & Intelligence Platform</span>
          <div className="ms-auto d-flex align-items-center gap-3">
            <span className="badge bg-success-subtle text-success border border-success px-3 py-2">
              ● API Live & Connected
            </span>
          </div>
        </header>
        <main className="p-4 flex-grow-1">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
