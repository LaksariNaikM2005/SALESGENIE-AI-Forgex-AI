import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Sparkles, Send, Copy, Mail, MessageSquare, Globe, Check, PhoneCall, FileText, Filter, UserCheck, Layers, Target } from 'lucide-react';

const AIOutreach = () => {
  const [prospects, setProspects] = useState([]);
  const [selectedLeadId, setSelectedLeadId] = useState('');

  // Requirement 7: Ordered Outreach Parameter Filters
  const [form, setForm] = useState({
    lead_name: 'Vikram Mehta',
    company_name: 'Apex Precision Robotics',
    industry: 'Industrial Automation',
    message_type: 'Executive Email', // Executive Email, LinkedIn Pitch, Phone Call Script, Commercial Proposal
    tone: 'Executive & Consultative', // Executive & Consultative, Technical & Engineering Heavy, ROI & Commercial Focus, Urgent Q4 Timeline
    value_prop: 'PLC & SCADA Integration', // PLC & SCADA Integration, Automation Efficiency & Throughput, Quality Control & Zero Defect, Enterprise Volume Pricing
    tech_stack: 'Siemens S7 PLC, ROS2, Fanuc CNC',
  });

  const [generated, setGenerated] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [status, setStatus] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    api.get('/leads?per_page=50')
      .then(res => {
        const list = res.data?.leads || res.data || [];
        setProspects(list);
        if (list.length > 0) {
          const l = list[0];
          setSelectedLeadId(l.id);
          setForm(prev => ({
            ...prev,
            lead_name: l.contact_name || 'Vikram Mehta',
            company_name: l.company || 'Apex Precision Robotics',
            industry: l.sector || 'Industrial Automation',
            tech_stack: l.tech_stack || 'Siemens PLC, ROS2',
          }));
        }
      })
      .catch(err => console.error(err));
  }, []);

  const handleSelectProspect = (leadId) => {
    setSelectedLeadId(leadId);
    const target = prospects.find(p => p.id === parseInt(leadId));
    if (target) {
      setForm(prev => ({
        ...prev,
        lead_name: target.contact_name || 'Prospect Lead',
        company_name: target.company,
        industry: target.sector || 'Industrial Automation',
        tech_stack: target.tech_stack || 'Siemens PLC, ROS2',
      }));
    }
  };

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
        recipient: `${form.lead_name.toLowerCase().replace(/[^a-z0-9]/g, '')}@${form.company_name.toLowerCase().replace(/[^a-z0-9]/g, '')}.com`,
        subject: generated.subject,
        body: generated.body,
      });
      setStatus(res.data.message);
    } catch (err) {
      alert('Failed to send outreach');
    } finally {
      setSending(false);
    }
  };

  const handleCopy = () => {
    if (!generated) return;
    navigator.clipboard.writeText(`${generated.subject}\n\n${generated.body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div>
      <div className="mb-4">
        <h2 className="fw-bold text-light mb-1 d-flex align-items-center gap-2">
          <Sparkles className="text-warning" size={28} /> AI Personalized Manufacturing Outreach
        </h2>
        <p className="text-muted mb-0">Generate hyper-personalized messaging using ordered parameter filters tailored for industrial manufacturing buyers</p>
      </div>

      <div className="row g-4">
        {/* Requirement 7: Input Parameters with Ordered Steps */}
        <div className="col-md-5">
          <div className="card border-secondary p-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center"><Filter className="me-2 text-primary" size={20} /> Ordered Outreach Parameter Filters</h5>
            <form onSubmit={handleGenerate}>
              {/* Step 1 */}
              <div className="mb-3 p-2 rounded border border-secondary bg-dark">
                <label className="form-label small fw-bold text-warning d-flex align-items-center gap-1">
                  <UserCheck size={14} /> Step 1: Target Prospect & Company
                </label>
                {prospects.length > 0 && (
                  <select
                    className="form-select form-select-sm bg-dark text-light border-secondary mb-2"
                    value={selectedLeadId}
                    onChange={e => handleSelectProspect(e.target.value)}
                  >
                    {prospects.map(p => (
                      <option key={p.id} value={p.id}>
                        {p.company} ({p.contact_name || 'Lead'}) — {p.sector}
                      </option>
                    ))}
                  </select>
                )}
                <div className="row g-2">
                  <div className="col-6">
                    <input
                      type="text"
                      className="form-control form-control-sm bg-dark text-light border-secondary"
                      value={form.lead_name}
                      onChange={e => setForm({ ...form, lead_name: e.target.value })}
                      placeholder="Lead Contact"
                      required
                    />
                  </div>
                  <div className="col-6">
                    <input
                      type="text"
                      className="form-control form-control-sm bg-dark text-light border-secondary"
                      value={form.company_name}
                      onChange={e => setForm({ ...form, company_name: e.target.value })}
                      placeholder="Company Name"
                      required
                    />
                  </div>
                </div>
              </div>

              {/* Step 2 */}
              <div className="mb-3 p-2 rounded border border-secondary bg-dark">
                <label className="form-label small fw-bold text-primary d-flex align-items-center gap-1">
                  <Mail size={14} /> Step 2: Campaign Channel
                </label>
                <select
                  className="form-select form-select-sm bg-dark text-light border-secondary fw-semibold"
                  value={form.message_type}
                  onChange={e => setForm({ ...form, message_type: e.target.value })}
                >
                  <option value="Executive Email">Executive Cold Email</option>
                  <option value="LinkedIn Pitch">LinkedIn Connection Pitch</option>
                  <option value="Phone Call Script">Phone Call Prospecting Script</option>
                  <option value="Commercial Proposal Cover Letter">Commercial Proposal Cover Letter</option>
                </select>
              </div>

              {/* Step 3 */}
              <div className="mb-3 p-2 rounded border border-secondary bg-dark">
                <label className="form-label small fw-bold text-info d-flex align-items-center gap-1">
                  <Layers size={14} /> Step 3: Communication Tone & Perspective
                </label>
                <select
                  className="form-select form-select-sm bg-dark text-light border-secondary fw-semibold"
                  value={form.tone}
                  onChange={e => setForm({ ...form, tone: e.target.value })}
                >
                  <option value="Executive & Consultative">Executive & Consultative (C-Level Operations)</option>
                  <option value="Technical & Engineering Heavy">Technical & Engineering Heavy (SCADA / PLC)</option>
                  <option value="ROI & Commercial Focus">ROI & Commercial Focus (Financial & Payback)</option>
                  <option value="Urgent Q4 Timeline">Urgent Q4 Timeline (Capacity & Discount Expiry)</option>
                </select>
              </div>

              {/* Step 4 */}
              <div className="mb-4 p-2 rounded border border-secondary bg-dark">
                <label className="form-label small fw-bold text-success d-flex align-items-center gap-1">
                  <Target size={14} /> Step 4: Primary Value Proposition Focus
                </label>
                <select
                  className="form-select form-select-sm bg-dark text-light border-secondary fw-semibold"
                  value={form.value_prop}
                  onChange={e => setForm({ ...form, value_prop: e.target.value })}
                >
                  <option value="PLC & SCADA Integration">PLC & SCADA Integration Roadmap</option>
                  <option value="Automation Efficiency & Throughput">Automation Efficiency & Line Throughput</option>
                  <option value="Quality Control & Zero Defect">Quality Control & Zero Defect Inspection</option>
                  <option value="Enterprise Volume Pricing">Enterprise Volume Pricing Tier</option>
                </select>
              </div>

              <button type="submit" className="btn btn-primary w-100 fw-semibold py-2 d-flex align-items-center justify-content-center gap-2" disabled={loading}>
                <Sparkles size={18} /> {loading ? 'Generating AI Copy...' : 'Generate Personalized Outreach'}
              </button>
            </form>
          </div>
        </div>

        {/* Generated Copy Preview & Review */}
        <div className="col-md-7">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 border-bottom border-secondary pb-2 d-flex align-items-center justify-content-between">
              <span>AI Generated Outreach Message</span>
              {generated && <span className="badge bg-primary-subtle text-primary border border-primary px-3">{generated.tone}</span>}
            </h5>
            {status && <div className="alert alert-success p-2 small">{status}</div>}

            {generated ? (
              <div className="d-flex flex-column h-100">
                <div className="mb-3">
                  <label className="form-label small text-muted">Subject Line / Call Header</label>
                  <input
                    type="text"
                    className="form-control bg-dark text-light border-secondary fw-semibold"
                    value={generated.subject}
                    onChange={e => setGenerated({ ...generated, subject: e.target.value })}
                  />
                </div>

                <div className="mb-4 flex-grow-1">
                  <label className="form-label small text-muted">Message Body ({form.message_type})</label>
                  <textarea
                    className="form-control bg-dark text-light border-secondary font-monospace"
                    rows="11"
                    value={generated.body}
                    onChange={e => setGenerated({ ...generated, body: e.target.value })}
                  ></textarea>
                </div>

                <div className="d-flex gap-2">
                  <button onClick={handleSend} className="btn btn-success fw-semibold d-flex align-items-center gap-2" disabled={sending}>
                    <Send size={18} /> {sending ? 'Dispatching...' : `Dispatch via ${form.message_type}`}
                  </button>
                  <button onClick={handleCopy} className="btn btn-outline-light d-flex align-items-center gap-2">
                    {copied ? <Check size={18} className="text-success" /> : <Copy size={18} />}
                    {copied ? 'Copied to Clipboard' : 'Copy Message'}
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center p-5 text-muted">
                <Mail size={48} className="mb-2 opacity-50 text-primary" />
                <p>Configure the 4 ordered parameter steps on the left and click "Generate Personalized Outreach".</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIOutreach;
