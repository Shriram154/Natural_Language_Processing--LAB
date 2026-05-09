import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, Loader2, Sparkles, Code2, Clock } from 'lucide-react';
import axios from 'axios';

const Dashboard = () => {
  const navigate = useNavigate();
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  const handleAnalyze = async () => {
    if (!code.trim()) return;
    
    setIsAnalyzing(true);
    setAnalysisResult(null);

    const token = localStorage.getItem('access_token');
    
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/api/analyze-code`,
        { code, language },
        { headers: { Authorization: `Bearer ${token}` }}
      );
      setAnalysisResult(response.data.analysis);
    } catch (error) {
      console.error("Analysis Failed:", error);
      alert("Failed to analyze code. Make sure the backend server is running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="container animate-fade-in">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2 className="gradient-text">Chatbot Dashboard</h2>
        <button onClick={handleLogout} className="btn-secondary" style={{ padding: '8px 16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <LogOut size={16} /> Logout
        </button>
      </header>

      <div className="dashboard-grid">
        {/* Input Area */}
        <div className="glass-panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Code2 size={20} color="var(--accent-color)" /> Code Input</h3>
            <select 
              value={language} 
              onChange={e => setLanguage(e.target.value)}
              style={{ background: 'rgba(0,0,0,0.5)', color: 'white', border: '1px solid var(--glass-border)', borderRadius: '4px', padding: '4px 8px' }}
            >
              <option value="python">Python</option>
              <option value="java">Java</option>
            </select>
          </div>
          
          <textarea 
            className="editor-container" 
            placeholder="Paste your Java or Python code here..."
            value={code}
            onChange={e => setCode(e.target.value)}
          />

          <button 
            className="btn-primary" 
            style={{ width: '100%', marginTop: '1rem', justifyContent: 'center' }}
            onClick={handleAnalyze}
            disabled={isAnalyzing || !code.trim()}
          >
            {isAnalyzing ? <><Loader2 className="animate-spin" size={20} /> Analyzing...</> : <><Sparkles size={20} /> Analyze Code</>}
          </button>
        </div>

        {/* Output Area */}
        <div className="glass-panel" style={{ overflowY: 'auto', maxHeight: '600px' }}>
          <h3 style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles size={20} color="#00d4ff" /> AI Analysis
          </h3>
          
          {!analysisResult && !isAnalyzing && (
            <div style={{ display: 'flex', height: '80%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
              Submit code to see the AI review here.
            </div>
          )}

          {isAnalyzing && (
            <div style={{ display: 'flex', flexDirection: 'column', height: '80%', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
              <Loader2 className="animate-spin" size={40} style={{ marginBottom: '1rem', color: 'var(--accent-color)' }} />
              <p>Hugging Face Models are analyzing your code...</p>
            </div>
          )}

          {analysisResult && (
            <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              
              <div>
                <h4 style={{ color: 'var(--accent-color)', marginBottom: '0.5rem' }}>Overview</h4>
                <p style={{ color: '#e0e0e0', fontSize: '0.95rem', lineHeight: '1.5' }}>{analysisResult.general_explanation}</p>
              </div>



              <div>
                <h4 style={{ color: 'var(--accent-color)', marginBottom: '0.5rem' }}>Line-by-Line Breakdown</h4>
                <pre style={{ whiteSpace: 'pre-wrap', background: 'rgba(0,0,0,0.3)', padding: '12px', borderRadius: '8px', fontSize: '0.85rem', color: '#c0c0c0', border: '1px solid var(--glass-border)' }}>
                  {analysisResult.line_by_line_explanation}
                </pre>
              </div>
              
              <div style={{ height: '1px', background: 'var(--glass-border)', margin: '1rem 0' }} />

              <div>
                <h4 style={{ color: '#00d4ff', marginBottom: '0.5rem' }}>Optimized Code</h4>
                <pre style={{ whiteSpace: 'pre-wrap', background: '#1e1e24', padding: '12px', borderRadius: '8px', fontSize: '0.85rem', color: '#e0e0e0', border: '1px solid var(--glass-border)' }}>
                  {analysisResult.optimized_code}
                </pre>
              </div>

              <div style={{ display: 'flex', gap: '1rem' }}>
                <div style={{ flex: 1 }}>
                  <h4 style={{ color: '#00d4ff', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Clock size={16} /> Optimized Time Complexity
                  </h4>
                  <div style={{ padding: '8px 12px', background: 'rgba(0, 212, 255, 0.1)', borderRadius: '6px', fontFamily: 'monospace', color: '#00d4ff' }}>
                    {analysisResult.time_complexity_optimized}
                  </div>
                </div>
              </div>

              <div>
                <h4 style={{ color: '#00d4ff', marginBottom: '0.5rem' }}>Why is it better?</h4>
                <p style={{ color: '#e0e0e0', fontSize: '0.95rem', lineHeight: '1.5' }}>{analysisResult.optimization_explanation}</p>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
