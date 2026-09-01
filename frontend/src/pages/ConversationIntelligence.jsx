import React, { useState } from 'react';
import api from '../services/api';
import { MessageSquareText, FileText, CheckSquare, DollarSign, ShieldAlert, Award } from 'lucide-react';

const ConversationIntelligence = () => {
  const [transcript, setTranscript] = useState(
    `Sales Rep: Hi Sarah, thanks for taking the time to speak with us today about Acme Tech Solutions' software needs.
Sarah Jenkins (CTO): Great to connect. We are looking to replace our current legacy CRM tool and improve our lead scoring accuracy.
Sales Rep: Fantastic. SalesGenie AI provides real-time scikit-learn lead scoring and GPT-4 conversation intelligence. What is your implementation timeframe and budget?
Sarah Jenkins (CTO): We have an approved budget of $45k-$60k for Q3. Our team is also reviewing Salesforce Einstein and HubSpot, but we want faster customization. We need a formal proposal and technical demo by next Tuesday.`
  );

  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSummarize = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/conversations/summarize', {
        title: 'CTO Demo & Strategy Call - Acme Tech',
        transcript: transcript,
      });
      setAnalysis(res.data);
    } catch (err) {
      alert('Failed to analyze transcript');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="mb-4">
        <h2 className="fw-bold text-light mb-1">Conversation & Meeting Intelligence</h2>
        <p className="text-muted mb-0">Summarize sales calls, extract action items, budget mentions, competitors, and sentiment</p>
      </div>

      <div className="row g-4">
        {/* Transcript Input */}
        <div className="col-md-5">
          <div className="card border-secondary p-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center"><FileText className="me-2 text-primary" size={20} /> Paste Call Transcript</h5>
            <form onSubmit={handleSummarize}>
              <div className="mb-3">
                <textarea
                  className="form-control bg-dark text-light border-secondary"
                  rows="12"
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Paste meeting transcript or call recording text here..."
                  required
                ></textarea>
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold py-2 d-flex align-items-center justify-content-center gap-2" disabled={loading}>
                <MessageSquareText size={18} /> {loading ? 'Extracting AI Insights...' : 'Analyze & Summarize Call'}
              </button>
            </form>
          </div>
        </div>

        {/* AI Conversation Output & Key Action Items */}
        <div className="col-md-7">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 border-bottom border-secondary pb-2">AI Conversation Insights</h5>

            {analysis ? (
              <div>
                <div className="d-flex align-items-center justify-content-between mb-3 p-3 rounded" style={{ backgroundColor: '#0f172a' }}>
                  <div>
                    <small className="text-muted d-block">Call Sentiment</small>
                    <span className="fw-bold text-success">{analysis.sentiment} ({analysis.sentiment_score * 100}%)</span>
                  </div>
                  <div>
                    <small className="text-muted d-block">Buyer Intent</small>
                    <span className="fw-bold text-primary">{analysis.customer_interest}</span>
                  </div>
                </div>

                <div className="mb-4">
                  <h6 className="fw-bold text-light">Meeting Summary:</h6>
                  <p className="p-3 rounded border border-secondary text-slate-300" style={{ backgroundColor: '#0f172a' }}>
                    {analysis.summary}
                  </p>
                </div>

                <div className="row g-3">
                  <div className="col-12">
                    <h6 className="fw-bold text-light d-flex align-items-center"><CheckSquare className="me-2 text-success" size={18} /> Action Items Extracted:</h6>
                    <ul className="list-group">
                      {analysis.insights?.filter(i => i.type === 'action_item').map((item, idx) => (
                        <li key={idx} className="list-group-item bg-dark text-light border-secondary">{item.content}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="col-6">
                    <h6 className="fw-bold text-light d-flex align-items-center"><DollarSign className="me-2 text-warning" size={18} /> Budget Mentions:</h6>
                    <ul className="list-group">
                      {analysis.insights?.filter(i => i.type === 'budget_mention').map((item, idx) => (
                        <li key={idx} className="list-group-item bg-dark text-light border-secondary small">{item.content}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="col-6">
                    <h6 className="fw-bold text-light d-flex align-items-center"><ShieldAlert className="me-2 text-danger" size={18} /> Competitors Mentioned:</h6>
                    <ul className="list-group">
                      {analysis.insights?.filter(i => i.type === 'competitor_mention').map((item, idx) => (
                        <li key={idx} className="list-group-item bg-dark text-light border-secondary small">{item.content}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center p-5 text-muted">
                <MessageSquareText size={48} className="mb-2 opacity-50" />
                <p>Click "Analyze & Summarize Call" to run AI conversation intelligence on the transcript.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationIntelligence;
