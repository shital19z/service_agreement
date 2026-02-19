import React, { useState } from 'react';

const ForgotPassword = ({ switchToLogin }) => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await fetch('http://127.0.0.1:8000/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ email: email.trim().toLowerCase() }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.message || 'Password reset email sent!');
        setEmailSent(true);
      } else {
        setError(data.detail || 'Something went wrong');
      }
    } catch (err) {
      setError('Could not connect to the server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card" style={{ maxWidth: '400px' }}>
        <h2 className="auth-logo">Service Agreement <span>Password Reset</span></h2>
        <p className="auth-subtitle">Enter your email to reset your password</p>

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

        {!emailSent ? (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="auth-label">Email Address</label>
              <input
                type="email"
                className="auth-input"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading}
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
              disabled={loading}
              style={{
                width: '100%',
                padding: '14px',
                fontSize: '16px',
                fontWeight: '700',
                background: loading ? '#94a3b8' : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                cursor: loading ? 'not-allowed' : 'pointer',
                opacity: loading ? 0.7 : 1,
                marginBottom: '15px'
              }}
            >
              {loading ? 'Sending...' : 'Send Reset Link'}
            </button>
          </form>
        ) : (
          <div style={{ textAlign: 'center', margin: '20px 0' }}>
            <p style={{ color: '#4a5568', marginBottom: '20px' }}>
              Check your email for the reset link.
            </p>
            <button
              onClick={() => setEmailSent(false)}
              style={{
                background: 'none',
                border: 'none',
                color: '#4facfe',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}
            >
              Try another email
            </button>
          </div>
        )}

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
            Back to Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;