import React, { useState, useEffect } from 'react';

const ResetPassword = ({ switchToLogin }) => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState('');

  useEffect(() => {
    // Get token from URL
    const urlParams = new URLSearchParams(window.location.search);
    const tokenParam = urlParams.get('token');
    if (tokenParam) {
      setToken(tokenParam);
    } else {
      setError('Invalid reset link');
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    // Validate passwords
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:8000/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          token: token,
          new_password: password 
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage('Password reset successful! Redirecting to login...');
        setTimeout(() => {
          switchToLogin();
        }, 3000);
      } else {
        setError(data.detail || 'Failed to reset password');
      }
    } catch (err) {
      setError('Could not connect to the server');
    } finally {
      setLoading(false);
    }
  };

  if (!token && !error) {
    return (
      <div className="auth-wrapper">
        <div className="auth-card">
          <h2 className="auth-logo">Service Agreement</h2>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card" style={{ maxWidth: '400px' }}>
        <h2 className="auth-logo">Service Agreement <span>Reset Password</span></h2>
        <p className="auth-subtitle">Enter your new password</p>

        {error && (
          <div style={{ 
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

        {message && (
          <div style={{ 
            color: '#2f855a', 
            background: '#f0fff4', 
            padding: '12px', 
            borderRadius: '8px',
            fontSize: '14px', 
            marginBottom: '20px',
            border: '1px solid #9ae6b4',
            textAlign: 'center'
          }}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="auth-label">New Password</label>
            <input
              type="password"
              className="auth-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading || message}
              minLength={6}
              style={{
                width: '100%',
                padding: '14px',
                border: '2px solid #e2e8f0',
                borderRadius: '10px',
                fontSize: '15px',
                marginBottom: '15px'
              }}
            />
          </div>

          <div className="form-group">
            <label className="auth-label">Confirm Password</label>
            <input
              type="password"
              className="auth-input"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={loading || message}
              style={{
                width: '100%',
                padding: '14px',
                border: '2px solid #e2e8f0',
                borderRadius: '10px',
                fontSize: '15px',
                marginBottom: '20px'
              }}
            />
          </div>

          <button 
            type="submit" 
            className="auth-btn"
            disabled={loading || message}
            style={{
              width: '100%',
              padding: '14px',
              fontSize: '16px',
              fontWeight: '700',
              background: loading || message ? '#94a3b8' : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              cursor: (loading || message) ? 'not-allowed' : 'pointer',
              opacity: (loading || message) ? 0.7 : 1,
              marginBottom: '15px'
            }}
          >
            {loading ? 'Resetting...' : 'Reset Password'}
          </button>
        </form>

        <div style={{
          marginTop: '25px',
          textAlign: 'center',
          borderTop: '1px solid #e2e8f0',
          paddingTop: '20px'
        }}>
          <button 
            onClick={switchToLogin} 
            style={{
              background: 'none',
              border: 'none',
              color: '#4facfe',
              fontSize: '15px',
              fontWeight: '600',
              cursor: 'pointer'
            }}
          >
            ← Back to Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;