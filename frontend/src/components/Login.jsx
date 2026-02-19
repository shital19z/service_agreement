import React, { useState, useContext } from 'react';
import { AuthContext } from '../AuthContext';

const Login = ({ switchToSignup, switchToForgotPassword }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const { login } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formData = new URLSearchParams();
      formData.append('username', username.trim().toLowerCase());
      formData.append('password', password);

      const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded' 
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        
        if (login) {
          login(data.access_token, { username: data.username || username });
        } else {
          setError("Context Error: login function not found.");
        }
      } else {
        const errorData = await response.json();
        const msg = errorData.detail 
          ? (typeof errorData.detail === 'string' ? errorData.detail : "Login failed")
          : "Invalid username or password.";
        setError(msg);
      }
    } catch (err) {
      console.error("Detailed Login Error:", err);
      setError(`Login Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2 className="auth-logo">Service Agreement <span>Login</span></h2>
        <p className="auth-subtitle">Welcome back! Please enter your details.</p>
        
        {error && (
          <div className="error-message" style={{ 
            color: '#e53e3e', 
            background: '#fff5f5', 
            padding: '12px', 
            borderRadius: '8px',
            fontSize: '14px', 
            marginBottom: '20px',
            border: '1px solid #feb2b2',
            textAlign: 'center'
          }}>
            {error}
          </div>
        )}
        
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="auth-label">Username (Email)</label>
            <input 
              type="text" 
              className="auth-input"
              placeholder="Enter your email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label className="auth-label">Password</label>
            <input 
              type="password" 
              className="auth-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          
          {/* Forgot Password Link */}
          <div style={{ 
            display: 'flex', 
            justifyContent: 'flex-end', 
            marginBottom: '20px',
            marginTop: '5px'
          }}>
            <button 
              type="button"
              onClick={switchToForgotPassword}
              style={{
                background: 'none',
                border: 'none',
                color: '#4facfe',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                textDecoration: 'none',
                padding: '5px 0',
                transition: 'color 0.2s'
              }}
              onMouseEnter={(e) => e.target.style.color = '#2563eb'}
              onMouseLeave={(e) => e.target.style.color = '#4facfe'}
            >
              Forgot Password?
            </button>
          </div>

          <button 
            type="submit" 
            className="auth-btn"
            disabled={loading}
            style={{
              opacity: loading ? 0.7 : 1,
              cursor: loading ? 'not-allowed' : 'pointer',
              width: '100%',
              padding: '14px',
              fontSize: '16px',
              fontWeight: '700',
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              boxShadow: '0 4px 15px rgba(79, 172, 254, 0.3)',
              transition: 'all 0.2s'
            }}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="auth-footer" style={{
          marginTop: '25px',
          textAlign: 'center',
          borderTop: '1px solid #e2e8f0',
          paddingTop: '20px'
        }}>
          <p style={{ color: '#64748b', marginBottom: '10px' }}>
            Don't have an account yet?
          </p>
          <button 
            onClick={switchToSignup} 
            className="auth-link"
            style={{
              background: 'none',
              border: 'none',
              color: '#4facfe',
              fontSize: '15px',
              fontWeight: '700',
              cursor: 'pointer',
              textDecoration: 'underline',
              padding: '5px 10px'
            }}
          >
            Create New Account (Sign Up)
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;