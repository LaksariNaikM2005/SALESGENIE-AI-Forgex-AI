import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { RefreshCw, CheckCircle, Database, ArrowRightLeft, ShieldCheck } from 'lucide-react';

const CRMSync = () => {
  const [connections, setConnections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [message, setMessage] = useState('');

  const fetchStatus = () => {
    setLoading(true);
    api.get('/crm/status')
      .then(res => setConnections(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const handleSyncAll = async () => {
    setSyncing(true);
    setMessage('');
    try {
      const res = await api.post('/crm/sync', { provider: 'all' });
      setMessage(res.data.message);
      fetchStatus();
    } catch (err) {
      alert('Failed to execute CRM sync');
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 className="fw-bold text-light mb-1">CRM Integration & Synchronization</h2>
          <p className="text-muted mb-0">Manage Salesforce & HubSpot bi-directional connectors and sync pipelines</p>
        </div>
        <button className="btn btn-primary d-flex align-items-center gap-2" onClick={handleSyncAll} disabled={syncing}>
          <RefreshCw size={18} className={syncing ? 'spin' : ''} /> {syncing ? 'Synchronizing...' : 'Sync All CRMs Now'}
        </button>
      </div>

      {message && <div className="alert alert-success p-3 mb-4">{message}</div>}

      <div className="row g-4 mb-4">
        {loading ? (
          <div className="col-12 text-center p-5"><div className="spinner-border text-primary"></div></div>
        ) : (
          connections.map((c) => (
            <div key={c.id} className="col-md-6">
              <div className="card border-secondary p-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
                <div className="d-flex align-items-center justify-content-between mb-3">
                  <div className="d-flex align-items-center gap-3">
                    <Database className="text-primary" size={28} />
                    <div>
                      <h5 className="fw-bold mb-0 text-capitalize">{c.provider}</h5>
                      <small className="text-muted">{c.account_name}</small>
                    </div>
                  </div>
                  <span className="badge bg-success-subtle text-success border border-success px-3 py-2">
                    ● {c.sync_status}
                  </span>
                </div>
                <hr className="border-secondary" />
                <div className="d-flex justify-content-between align-items-center small">
                  <span className="text-muted">Last Synchronized:</span>
                  <span className="fw-semibold">{c.last_sync_at ? new Date(c.last_sync_at).toLocaleString() : 'Just now'}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      <div className="card border-secondary p-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
        <h5 className="fw-bold mb-3 d-flex align-items-center"><ShieldCheck className="me-2 text-success" size={20} /> Integration Security & Credentials</h5>
        <p className="text-muted small">All CRM API keys and OAuth tokens are stored using environment variable encryption and separated behind the FastAPI service boundary layer.</p>
      </div>
    </div>
  );
};

export default CRMSync;
