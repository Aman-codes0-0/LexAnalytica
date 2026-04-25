import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Upload, 
  Trash2, 
  RefreshCcw, 
  Settings, 
  Search, 
  FileTerminal, 
  ShieldCheck, 
  CheckCircle2, 
  ChevronDown,
  ChevronUp,
  Layout,
  Globe,
  Star,
  AlertTriangle
} from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
  return twMerge(clsx(inputs));
}

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [mode, setMode] = useState('both');
  const [outputLang, setOutputLang] = useState('en');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [originalTextCollapsed, setOriginalTextCollapsed] = useState(true);

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) validateAndSetFile(file);
  };

  const validateAndSetFile = (file) => {
    const validTypes = ['.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();

    if (!validTypes.includes(ext)) {
      alert('Unsupported file type. Please upload PDF, DOCX, TXT, or Image (PNG/JPG) files.');
      return;
    }

    if (file.size > 16 * 1024 * 1024) {
      alert('File too large. Maximum size is 16 MB.');
      return;
    }

    setSelectedFile(file);
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setLoadingStep(0);
    setResults(null);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('mode', mode);
    formData.append('output_lang', outputLang);

    const stepInterval = setInterval(() => {
      setLoadingStep(prev => (prev < 2 ? prev + 1 : prev));
    }, 2000);

    try {
      const response = await fetch('/api/summarize', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      clearInterval(stepInterval);

      if (!response.ok) {
        throw new Error(data.detail || 'Server error occurred.');
      }

      setResults(data);
      setLoading(false);
    } catch (err) {
      clearInterval(stepInterval);
      setError(err.message);
      setLoading(false);
    }
  };

  const reset = () => {
    setSelectedFile(null);
    setResults(null);
    setError(null);
    setLoading(false);
  };

  const [downloading, setDownloading] = useState(null); // 'pdf', 'docx' or null

  const handleDownload = async (format) => {
    if (!results || downloading) return;

    setDownloading(format);
    console.log(`[INFO] Starting ${format} download...`);

    try {
      const response = await fetch(`/api/download/${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(results),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || `Server returned ${response.status}`);
      }

      const blob = await response.blob();
      if (blob.size === 0) throw new Error("Received empty file from server");

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      
      // Sanitized filename
      const baseName = (results.filename || 'analysis').replace(/\.[^/.]+$/, "");
      a.download = `${baseName}_legal_summary.${format}`;
      
      document.body.appendChild(a);
      a.click();
      
      // Defer cleanup to ensure browser handles the click
      setTimeout(() => {
        window.URL.revokeObjectURL(url);
        a.remove();
        console.log(`[SUCCESS] ${format} download triggered.`);
      }, 150);

    } catch (err) {
      console.error(`[ERROR] ${format} download failed:`, err);
      alert(`Download failed: ${err.message}`);
    } finally {
      setDownloading(null);
    }
  };

  const loadingMessages = [
    'Parsing document structure...',
    'Extracting legal intelligence...',
    'Performing document synthesis...'
  ];

  const totalEntities = results ? Object.values(results.entities).reduce((acc, curr) => acc + (Array.isArray(curr) ? curr.length : 0), 0) : 0;

  return (
    <div className="flex flex-col">
      <nav className="navbar">
        <div className="nav-brand">
          <div className="nav-icon">
            <Layout size={20} />
          </div>
          <span className="nav-title">Lex<span className="highlight">Analytica</span></span>
        </div>
        <div className="nav-subtitle">Advanced Document Intelligence</div>
      </nav>

      <main className="container">
        {!results && !loading && !error && (
          <>
            <section className="hero">
              <div className="hero-badge">Enterprise Legal Technology</div>
              <h1 className="hero-title">
                Analyze Legal Documents <span className="gradient-text">with Precision</span>
              </h1>
              <p className="hero-desc">
                Automated summarization and entity extraction for legal professionals. 
                Process court judgments, contracts, and filings with institutional-grade NLP technology.
              </p>
              <div className="hero-stats">
                <div className="stat">
                  <span className="stat-value">PDF</span>
                  <span className="stat-label">Analysis</span>
                </div>
                <div className="stat-divider" />
                <div className="stat">
                  <span className="stat-value">DOCX</span>
                  <span className="stat-label">Synthesis</span>
                </div>
                <div className="stat-divider" />
                <div className="stat">
                  <span className="stat-value">NLP</span>
                  <span className="stat-label">Extraction</span>
                </div>
              </div>
            </section>

            <section className="upload-section">
              <div className="section-header">
                <h2 className="section-title">Document Analysis</h2>
                <p className="section-desc">Select a document to begin processing.</p>
              </div>

              <form onSubmit={handleSubmit}>
                <div 
                  className="dropzone"
                  onClick={() => document.getElementById('file-input').click()}
                >
                  <Upload className="dropzone-icon" size={48} />
                  <h3 className="dropzone-text">Click to upload or drag & drop</h3>
                  <p className="dropzone-subtext">Supports PDF, DOCX, TXT, and Images (Max 16MB)</p>
                  <input 
                    type="file" 
                    id="file-input" 
                    hidden 
                    accept=".pdf,.docx,.txt,.png,.jpg,.jpeg"
                    onChange={handleFileChange}
                  />
                </div>

                {selectedFile && (
                  <div className="file-info">
                    <div className="file-icon">📄</div>
                    <div className="file-details">
                      <div className="file-name">{selectedFile.name}</div>
                      <div className="file-size">{formatBytes(selectedFile.size)}</div>
                    </div>
                    <button 
                      type="button" 
                      onClick={reset}
                      className="file-remove"
                    >
                      <Trash2 size={20} />
                    </button>
                  </div>
                )}

                <div className="mode-selector">
                  <span className="mode-label">Analysis Mode</span>
                  <div className="mode-options">
                    {[
                      { id: 'both', name: 'Full Analysis', icon: '📜', desc: 'Extractive + Abstractive' },
                      { id: 'extractive', name: 'Extractive', icon: '🔍', desc: 'Direct Evidence' },
                      { id: 'abstractive', name: 'Synthesis', icon: '📑', desc: 'Document Synthesis' }
                    ].map(opt => (
                      <label key={opt.id} className="mode-option">
                        <input 
                          type="radio" 
                          name="mode" 
                          value={opt.id} 
                          className="hidden" 
                          checked={mode === opt.id}
                          onChange={(e) => setMode(e.target.value)}
                        />
                        <div className="mode-btn">
                          <span className="mode-icon">{opt.icon}</span>
                          <span className="mode-name">{opt.name}</span>
                          <span className="mode-desc">{opt.desc}</span>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                <div className="mode-selector">
                  <span className="mode-label">Output Language</span>
                  <div className="mode-options" style={{ gridTemplateColumns: '1fr 1fr' }}>
                    {[
                      { id: 'en', name: 'English', icon: '🇬🇧', desc: 'Results in English' },
                      { id: 'hi', name: 'Hindi (हिन्दी)', icon: '🇮🇳', desc: 'परिणाम हिन्दी में' }
                    ].map(opt => (
                      <label key={opt.id} className="mode-option">
                        <input 
                          type="radio" 
                          name="output_lang" 
                          value={opt.id} 
                          className="hidden" 
                          checked={outputLang === opt.id}
                          onChange={(e) => setOutputLang(e.target.value)}
                        />
                        <div className="mode-btn">
                          <span className="mode-icon">{opt.icon}</span>
                          <span className="mode-name">{opt.name}</span>
                          <span className="mode-desc">{opt.desc}</span>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                <button 
                  type="submit" 
                  disabled={!selectedFile || loading}
                  className="submit-btn"
                >
                  {loading ? <RefreshCcw className="animate-spin" size={20} /> : 'Process Document'}
                </button>
              </form>
            </section>
          </>
        )}

        {loading && (
          <section className="flex flex-col items-center justify-center py-20 animate-fadeIn">
            <div className="loading-indicator mb-8">
              <div className="loading-circle-bg" />
              <div className="loading-circle-active animate-spin" />
            </div>
            <div className="text-center">
              <h3 className="text-xl font-bold mb-2">Analyzing Document</h3>
              <p className="text-muted">{loadingMessages[loadingStep]}</p>
            </div>
            <div className="flex gap-10 mt-10">
              {['Text Extraction', 'Intel Extraction', 'Synthesis'].map((step, i) => (
                <div key={step} className="flex flex-col items-center gap-2">
                  <div className={cn(
                    "step-dot",
                    loadingStep > i ? "completed" : 
                    loadingStep === i ? "active animate-pulse" : 
                    "pending"
                  )} />
                  <span className={cn(
                    "text-xs font-medium",
                    loadingStep >= i ? "text-primary" : "text-muted"
                  )}>{step}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {error && (
          <section className="py-20 animate-fadeIn">
            <div className="p-10 bg-secondary border border-danger/30 rounded-lg text-center">
              <div className="text-4xl mb-4 text-danger">⚠️</div>
              <h3 className="text-xl font-bold mb-2">Processing Error</h3>
              <p className="text-danger mb-8">{error}</p>
              <button 
                onClick={reset}
                className="new-analysis-btn"
                style={{ marginTop: 0 }}
              >
                Try Again
              </button>
            </div>
          </section>
        )}

        {results && !loading && (
          <section className="results-section animate-fadeIn">
            <div className="section-header flex justify-between items-center">
              <div>
                <h2 className="section-title">Analysis Results</h2>
                <p className="section-desc">Extracted insights and document synthesis.</p>
              </div>
              <div className="flex gap-2">
                <button 
                  onClick={() => handleDownload('pdf')}
                  disabled={!!downloading}
                  className="px-4 py-2 bg-[#6366f1]/10 text-[#818cf8] border border-[#6366f1]/20 rounded-md text-sm font-medium hover:bg-[#6366f1]/20 transition-colors flex items-center gap-2 disabled:opacity-50"
                >
                  {downloading === 'pdf' ? <RefreshCcw size={16} className="animate-spin" /> : <FileText size={16} />}
                  {downloading === 'pdf' ? 'Preparing...' : 'Download PDF'}
                </button>
              </div>
            </div>

            <div className="stats-grid">
              {[
                { icon: '📊', val: results.word_count, label: 'Words' },
                { icon: '📑', val: results.sentence_count, label: 'Sentences' },
                { icon: '⏳', val: results.text_length, label: 'Characters' },
                { icon: '🛡️', val: totalEntities, label: 'Entities' },
                { icon: '🕸️', val: results.graph_stats?.total_nodes || 0, label: 'Graph Nodes' }
              ].map(stat => (
                <div key={stat.label} className="stat-card">
                  <span className="stat-card-icon">{stat.icon}</span>
                  <span className="stat-card-value">{stat.val?.toLocaleString() || 0}</span>
                  <span className="stat-card-label">{stat.label}</span>
                </div>
              ))}
            </div>

            <div className="result-panel">
              <div className="panel-header">
                <h3 className="panel-title">
                  <ShieldCheck size={20} />
                  Identified Entities
                </h3>
              </div>
              <div className="p-5">
                {totalEntities > 0 ? (
                  <div className="flex flex-col gap-6">
                    {[
                      { key: 'persons', label: '👤 Persons', color: 'bg-[#6366f1]/10 text-[#818cf8]' },
                      { key: 'organizations', label: '🏛️ Organizations', color: 'bg-[#10b981]/10 text-[#34d399]' },
                      { key: 'dates', label: '📅 Dates', color: 'bg-[#f59e0b]/10 text-[#fbbf24]' },
                      { key: 'locations', label: '📍 Locations', color: 'bg-[#ef4444]/10 text-[#f87171]' },
                      { key: 'case_numbers', label: '📂 Case Numbers', color: 'bg-[#8b5cf6]/10 text-[#a78bfa]' },
                      { key: 'law_sections', label: '⚖️ Law Sections', color: 'bg-[#ec4899]/10 text-[#f472b6]' },
                    ].map(group => {
                      const items = results.entities[group.key];
                      if (!items || items.length === 0) return null;
                      return (
                        <div key={group.key}>
                          <div className="text-xs font-semibold text-secondary mb-2" style={{ color: 'var(--text-secondary)' }}>{group.label}</div>
                          <div className="flex flex-wrap gap-2">
                            {items.map((item, idx) => (
                              <span key={idx} className={cn("px-3 py-1 rounded text-xs font-medium border border-white/5", group.color)}>
                                {item}
                              </span>
                            ))}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-center py-4 text-muted">No entities identified in this document.</p>
                )}
              </div>
            </div>

            {results.summary.extractive && (
              <div className="result-panel">
                <div className="panel-header">
                  <h3 className="panel-title">
                    <FileText size={20} />
                    Summary
                  </h3>
                  <span className="panel-badge">Analysis</span>
                </div>
                <div className="p-5">
                  <p className="summary-text italic border-l-2 pl-4">
                    {results.summary.extractive}
                  </p>
                </div>
              </div>
            )}

            {results.summary.abstractive && (
              <div className="result-panel">
                <div className="panel-header">
                  <h3 className="panel-title">
                    <Star size={20} />
                    Abstractive Summary
                  </h3>
                  <span className="panel-badge ai-badge">AI Generated</span>
                </div>
                <div className="p-5">
                   <p className="summary-text">
                    {results.summary.abstractive}
                  </p>
                </div>
              </div>
            )}

            {results.reasoning_deductions && results.reasoning_deductions.length > 0 && (
              <div className="result-panel">
                <div className="panel-header" style={{ borderColor: 'rgba(239, 68, 68, 0.2)' }}>
                  <h3 className="panel-title text-danger">
                    <AlertTriangle size={20} />
                    Neurosymbolic Deductions
                  </h3>
                  <span className="panel-badge" style={{ background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444' }}>Logic Engine</span>
                </div>
                <div className="p-5">
                  <div className="flex flex-col gap-3">
                    {results.reasoning_deductions.map((deduction, idx) => (
                      <div key={idx} className="p-4 rounded-md border border-white/10 bg-black/20">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-xs font-bold font-mono text-secondary">{deduction.rule_id}</span>
                          <span className={cn(
                            "text-xs px-2 py-0.5 rounded font-bold",
                            deduction.severity === 'HIGH' ? "bg-danger/20 text-danger" : 
                            deduction.severity === 'MEDIUM' ? "bg-warning/20 text-warning" : "bg-info/20 text-info"
                          )}>{deduction.severity}</span>
                        </div>
                        <p className="text-sm">{deduction.conclusion}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            <div className="result-panel">
                <div 
                  className="panel-header"
                  style={{ cursor: 'pointer' }}
                  onClick={() => setOriginalTextCollapsed(!originalTextCollapsed)}
                >
                  <h3 className="panel-title">
                    <FileTerminal size={20} />
                    Original Text Preview
                  </h3>
                  {originalTextCollapsed ? <ChevronDown size={18} /> : <ChevronUp size={18} />}
                </div>
                {!originalTextCollapsed && (
                  <div className="p-5 border-t" style={{ maxHeight: '400px', overflowY: 'auto' }}>
                    <p className="original-text whitespace-pre-wrap">
                      {results.original_text}
                    </p>
                  </div>
                )}
            </div>

            <button 
              onClick={reset}
              className="submit-btn"
              style={{ background: '#475569' }}
            >
              <RefreshCcw size={20} />
              Analyze Another Document
            </button>
          </section>
        )}
      </main>

      <footer className="footer mt-auto">
        <p className="font-semibold mb-1">LexAnalytica Institutional Document Analytics</p>
        <p className="footer-tech">Engineered for Legal Accuracy • Powered by NLP Intelligence</p>
      </footer>
    </div>
  );
}
