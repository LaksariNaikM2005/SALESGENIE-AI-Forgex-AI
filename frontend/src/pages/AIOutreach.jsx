import React, { useState } from 'react';
import api from '../services/api';
import { Sparkles, Send, Copy, Mail, Globe } from 'lucide-react';

const AIOutreach = () => {
  const [form, setForm] = useState({
    lead_name: 'Sarah Jenkins',
    company_name: 'Acme Tech Solutions',
    industry: 'Software & IT',
    message_type: 'cold_email',
  });

  const [generated, setGenerated] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState('');

  const handleGenerate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setStatus('');
    try {
      const res = await api.post('/outreach/generate', form);
      setGenerated(res.data);
    } catch (err) {
      alert('Failed to generate outreach content');
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!generated) return;
    setSending(true);
    try {
      const res = await api.post('/outreach/send', {
        recipient: `${form.lead_name.toLowerCase().replace(' ', '.')}@${form.company_name.toLowerCase().replace(/[^a-z0-9]/g, '')}.com`,
        subject: generated.subject,
        body: generated.body,
      });
      setStatus(res.data.message);
    } catch (err) {
      alert('Failed to send email');
    } finally {
      setSending(false);
    }
  };

  return (
    <div>
      <div className="mb-4">
        <h2 className="fw-bold text-light mb-1">AI Personalized Outreach Generator</h2>
        <p className="text-muted mb-0">Generate hyper-personalized cold emails, follow-ups, and LinkedIn pitches with GPT-3.5/4</p>
      </div>

      <div className="row g-4">
        {/* Input Form */}
        <div className="col-md-5">
          <div className="card border-secondary p-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center"><Sparkles className="me-2 text-primary" size={20} /> Parameters</h5>
            <form onSubmit={handleGenerate}>
              <div className="mb-3">
                <label className="form-label small text-muted">Recipient Name</label>
                <input
                  type="text"
                  className="form-control bg-dark text-light border-secondary"
                  value={form.lead_name}
                  onChange={e => setForm({ ...form, lead_name: e.target.value })}
                  required
                />
              </div>

              <div className="mb-3">
                <label className="form-label small text-muted">Company Name</label>
                <input
                  type="text"
                  className="form-control bg-dark text-light border-secondary"
                  value={form.company_name}
                  onChange={e => setForm({ ...form, company_name: e.target.value })}
                  required
                />
              </div>

              <div className="mb-3">
                <label className="form-label small text-muted">Industry</label>
                <input
                  type="text"
                  className="form-control bg-dark text-light border-secondary"
                  value={form.industry}
                  onChange={e => setForm({ ...form, industry: e.target.value })}
                  required
                />
              </div>

              <div className="mb-4">
                <label className="form-label small text-muted">Message Format</label>
                <select
                  className="form-select bg-dark text-light border-secondary"
                  value={form.message_type}
                  onChange={e => setForm({ ...form, message_type: e.target.value })}
                >
                  <option value="cold_email">Cold Email</option>
                  <option value="follow_up">Follow-Up Email</option>
                  <option value="linkedin_pitch">LinkedIn Connection Message</option>
                </select>
              </div>

              <button type="submit" className="btn btn-primary w-100 fw-semibold py-2 d-flex align-items-center justify-content-center gap-2" disabled={loading}>
                <Sparkles size={18} /> {loading ? 'Generating with AI...' : 'Generate Outreach Copy'}
              </button>
            </form>
          </div>
        </div>

        {/* Generated Copy Preview & Review */}
        <div className="col-md-7">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 border-bottom border-secondary pb-2">AI Generated Copy & Review</h5>
            {status && <div className="alert alert-success p-2 small">{status}</div>}

            {generated ? (
              <div className="d-flex flex-column h-100">
                <div className="mb-3">
                  <label className="form-label small text-muted">Subject Line</label>
                  <input
                    type="text"
                    className="form-control bg-dark text-light border-secondary fw-semibold"
                    value={generated.subject}
                    onChange={e => setGenerated({ ...generated, subject: e.target.value })}
                  />
                </div>

                <div className="mb-4 flex-grow-1">
                  <label className="form-label small text-muted">Body Message</label>
                  <textarea
                    className="form-control bg-dark text-light border-secondary"
                    rows="8"
                    value={generated.body}
                    onChange={e => setGenerated({ ...generated, body: e.target.value })}
                  ></textarea>
                </div>

                <div className="d-flex gap-2">
                  <button onClick={handleSend} className="btn btn-success fw-semibold d-flex align-items-center gap-2" disabled={sending}>
                    <Send size={18} /> {sending ? 'Sending...' : 'Approve & Send Email'}
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center p-5 text-muted">
                <Mail size={48} className="mb-2 opacity-50" />
                <p>Fill in parameters and click "Generate Outreach Copy" to generate customized AI messaging.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIOutreach;
