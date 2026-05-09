import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Auth = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Configure axios
    const API_URL = `${import.meta.env.VITE_API_URL || "http://localhost:8000"}/auth`;

    try {
      if (isLogin) {
        // We will just use the UserCreate format for our quick mini-project login
        const response = await axios.post(`${API_URL}/login`, {
          username: formData.email, // Fast API implementation usually requires oauth format, but we used custom schema
          email: formData.email,
          password: formData.password
        });
        localStorage.setItem('access_token', response.data.access_token);
        navigate('/dashboard');
      } else {
        const response = await axios.post(`${API_URL}/signup`, formData);
        if (response.data) {
          // Automatically log in using the same credentials
          const loginResponse = await axios.post(`${API_URL}/login`, {
            username: formData.email,
            email: formData.email,
            password: formData.password
          });
          localStorage.setItem('access_token', loginResponse.data.access_token);
          navigate('/dashboard');
        }
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication Failed. Please check your credentials.");
    }
  };

  return (
    <div className="container animate-fade-in" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 style={{ marginBottom: '1.5rem', textAlign: 'center' }} className="gradient-text">
          {isLogin ? 'Welcome Back' : 'Create an Account'}
        </h2>
        
        {error && (
          <div style={{ padding: '10px', backgroundColor: 'rgba(255, 50, 50, 0.2)', color: '#ffaaaa', borderRadius: '8px', marginBottom: '1rem', fontSize: '0.875rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="form-group">
              <label className="form-label">Username</label>
              <input 
                type="text" 
                className="form-input"
                required={!isLogin}
                value={formData.username}
                onChange={e => setFormData({...formData, username: e.target.value})}
              />
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Email</label>
            <input 
              type="email" 
              className="form-input" 
              required
              value={formData.email}
              onChange={e => setFormData({...formData, email: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input 
              type="password" 
              className="form-input" 
              required
              value={formData.password}
              onChange={e => setFormData({...formData, password: e.target.value})}
            />
          </div>

          <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: '1rem' }}>
            {isLogin ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>
            {isLogin ? "Don't have an account? " : "Already have an account? "}
            <span 
              onClick={() => { setIsLogin(!isLogin); setError(''); }}
              style={{ color: 'var(--accent-color)', cursor: 'pointer', fontWeight: 'bold' }}
            >
              {isLogin ? "Sign Up" : "Log In"}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Auth;
