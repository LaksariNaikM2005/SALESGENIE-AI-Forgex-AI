import React, { useState } from 'react';
import api from '../services/api';
import { MessageSquareText, FileText, CheckSquare, DollarSign, ShieldAlert, Zap, Radio, Smile, Meh, Frown } from 'lucide-react';

const SAMPLE_TRANSCRIPTS = {
  positive: `Sales Rep: Hi Sarah, thanks for joining today's executive demo of SalesGenie AI.
Sarah Jenkins (CTO): Great to connect. We are looking to replace our current legacy CRM tool and improve our lead scoring accuracy.
Sales Rep: Fantastic. SalesGenie AI provides real-time scikit-learn lead scoring and GPT-4 conversation intelligence. What is your implementation timeframe and budget?
Sarah Jenkins (CTO): We have an approved budget of $45k-$60k for Q3. Our team is also reviewing Salesforce Einstein and HubSpot, but we want faster customization. We need a formal proposal and technical demo by next Tuesday.`,

  negative: `Sales Rep: Hi Mark, thanks for jumping on the call to discuss SalesGenie AI.
Mark Davis (VP Sales): Honestly, our team had a terrible experience with our last AI scoring software. It misclassified 40% of our high-value leads.
Sales Rep: I understand your frustration. Our model uses customized Random Forest classifiers trained on your actual closed-won data.
Mark Davis (VP Sales): We are very skeptical. We are currently locked into a contract with Competitor CRM until December and our budget is frozen. I don't think we can move forward right now.`,

  neutral: `Sales Rep: Hi Ellen, reaching out regarding your inquiry about B2B sales automation.
Ellen Vance (Operations): We are evaluating several tools for Q4 benchmarking. Just gathering feature comparison matrix and documentation.
Sales Rep: Perfect. Would you like to review our automated follow-ups and CRM sync capabilities?
Ellen Vance (Operations): Please send the whitepaper to my email. We will review it internally during our quarterly planning meeting.`
};

const ConversationIntelligence = () => {
  const [transcript, setTranscript] = useState(SAMPLE_TRANSCRIPTS.positive);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [simulating, setSimulating] = useState(false);

  const handleSummarize = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/conversations/summarize', {
        title: 'Executive Meeting & Discovery Call',
        transcript: transcript,
      });
      setAnalysis(res.data);
    } catch (err) {
      alert('Failed to analyze transcript');
    } finally {
      setLoading(false);
    }
  };

  const handleSimulateLiveStream = () => {
    setSimulating(true);
    setTranscript('');
    let index = 0;
    const fullText = SAMPLE_TRANSCRIPTS.positive;
    const interval = setInterval(() => {
      if (index < fullText.length) {
        setTranscript(prev => prev + fullText.charAt(index));
        index += 3;
      } else {
        clearInterval(interval);
        setSimulating(false);
        setTranscript(fullText);
      }
    }, 30);
  };

  const getToneBadge = (sentimentScore, sentimentText) => {
    const text = (sentimentText || '').toLowerCase();
    if (text.includes('positive') || sentimentScore >= 0.7) {
      return { label: 'Positive (+ve)', color: 'bg-success text-white', icon: Smile };
    }
    if (text.includes('negative') || sentimentScore <= 0.4) {
      return { label: 'Negative (-ve)', color: 'bg-danger text-white', icon: Frown };
    }
    return { label: 'Neutral', color: 'bg-warning text-dark', icon: Meh };
  };

  return (
    <div>
      <div className="mb-4">
        <h2 className="fw-bold text-light mb-1">Conversation & Meeting Intelligence</h2>
        <p className="text-muted mb-0">Automated live transcription, tone nature detection (+ve, -ve, Neutral), and GPT key insight extraction</p>
      </div>

      {/* Preset Transcript Toolbar */}
      <div className="card border-secondary p-3 mb-4" style={{ backgroundColor: '#1e293b' }}>
        <div className="d-flex align-items-center justify-content-between flex-wrap gap-2">
          <div className="d-flex align-items-center gap-2">
            <span className="small text-muted fw-medium">Load Preset Call Script:</span>
            <button className="btn btn-sm btn-outline-success" onClick={() => setTranscript(SAMPLE_TRANSCRIPTS.positive)}>
              <Smile size={14} className="me-1" /> High Intent (+ve)
            </button>
            <button className="btn btn-sm btn-outline-warning" onClick={() => setTranscript(SAMPLE_TRANSCRIPTS.neutral)}>
              <Meh size={14} className="me-1" /> Inquiry (Neutral)
            </button>
            <button className="btn btn-sm btn-outline-danger" onClick={() => setTranscript(SAMPLE_TRANSCRIPTS.negative)}>
              <Frown size={14} className="me-1" /> Skeptical (-ve)
            </button>
          </div>
          <button onClick={handleSimulateLiveStream} className="btn btn-sm btn-outline-info d-flex align-items-center gap-1" disabled={simulating}>
            <Radio size={14} className={simulating ? 'text-danger animate-pulse' : ''} />
            {simulating ? 'Transcribing Live Audio Stream...' : 'Simulate Live Mic Stream'}
          </button>
        </div>
      </div>

      <div className="row g-4">
        {/* Transcript Input */}
        <div className="col-md-5">
          <div className="card border-secondary p-4" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 d-flex align-items-center"><FileText className="me-2 text-primary" size={20} /> Automated Call Transcript</h5>
            <form onSubmit={handleSummarize}>
              <div className="mb-3">
                <textarea
                  className="form-control bg-dark text-light border-secondary font-monospace small"
                  rows="12"
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Paste meeting transcript or click 'Simulate Live Mic Stream'..."
                  required
                ></textarea>
              </div>
              <button type="submit" className="btn btn-primary w-100 fw-semibold py-2 d-flex align-items-center justify-content-center gap-2" disabled={loading || simulating}>
                <MessageSquareText size={18} /> {loading ? 'Analyzing Tone & Extracting Insights...' : 'Analyze & Detect Tone Nature'}
              </button>
            </form>
          </div>
        </div>

        {/* AI Conversation Output & Key Action Items */}
        <div className="col-md-7">
          <div className="card border-secondary p-4 h-100" style={{ backgroundColor: '#1e293b', color: '#f8fafc' }}>
            <h5 className="fw-bold mb-3 border-bottom border-secondary pb-2">AI Tone Nature & Call Insights</h5>

            {analysis ? (
              <div>
                {/* Tone Nature Header */}
                <div className="d-flex align-items-center justify-content-between mb-4 p-3 rounded" style={{ backgroundColor: '#0f172a' }}>
                  <div>
                    <small className="text-muted d-block mb-1">Tone Nature Detection</small>
                    {(() => {
                      const toneInfo = getToneBadge(analysis.sentiment_score, analysis.sentiment);
                      const Icon = toneInfo.icon;
                      return (
                        <span className={`badge ${toneInfo.color} px-3 py-2 fs-6 d-inline-flex align-items-center gap-2`}>
                          <Icon size={18} /> {toneInfo.label}
                        </span>
                      );
                    })()}
                  </div>
                  <div>
                    <small className="text-muted d-block mb-1">Confidence Score</small>
                    <span className="fw-bold text-light fs-5">{(analysis.sentiment_score * 100).toFixed(0)}%</span>
                  </div>
                  <div>
                    <small className="text-muted d-block mb-1">Buyer Intent Level</small>
                    <span className="fw-bold text-primary fs-5">{analysis.customer_interest}</span>
                  </div>
                </div>

                <div className="mb-4">
                  <h6 className="fw-bold text-light">Executive Summary:</h6>
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
                <MessageSquareText size={48} className="mb-2 opacity-50 text-primary" />
                <p>Click "Analyze & Detect Tone Nature" to run AI conversation intelligence on the transcript.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationIntelligence;
