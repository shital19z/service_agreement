import React, { useState } from 'react';

const Signup = ({ switchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    role: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await fetch('http://127.0.0.1:8000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({
          username: formData.username.trim().toLowerCase(),
          password: formData.password,
          role: formData.role || 'Responsible Party'
        }),
      });

      if (response.ok) {
        setSuccess('Account created successfully! Redirecting to login...');
        setTimeout(() => {
          switchToLogin();
        }, 2000);
      } else {
        const errorData = await response.json();
        const msg = typeof errorData.detail === 'string' 
          ? errorData.detail 
          : "Signup failed. Please try again.";
        setError(msg);
      }
    } catch (err) {
      setError('Could not connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h1 className="auth-logo">Care<span>Portal</span></h1>
        <p className="auth-subtitle">Create your account to manage agreements</p>

        {/* Beautiful Alert Messages */}
        {error && (
          <div className="custom-alert alert-error">
            <div className="alert-icon">⚠️</div>
            <div className="alert-content">
              <div className="alert-title">Error</div>
              <div className="alert-message">{error}</div>
            </div>
            <button className="alert-close" onClick={() => setError('')}>×</button>
          </div>
        )}

        {success && (
          <div className="custom-alert alert-success">
            <div className="alert-icon">✅</div>
            <div className="alert-content">
              <div className="alert-title">Success</div>
              <div className="alert-message">{success}</div>
            </div>
            <button className="alert-close" onClick={() => setSuccess('')}>×</button>
          </div>
        )}

        <form onSubmit={handleSignup}>
          <div className="form-group">
            <label className="auth-label">Username (Email)</label>
            <input
              type="text"
              className="auth-input"
              placeholder="Enter your email"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
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
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              required
              disabled={loading}
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label className="auth-label">Your Role</label>
            <select
              className="auth-input"
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
              disabled={loading}
              required
            >
              <option value="" disabled>-- Select your role --</option>
              <option value="Responsible Party">Responsible Party</option>
              <option value="Care Recipient">Care Recipient</option>
              <option value="Agent">Agent</option>
            </select>
          </div>

          <button 
            type="submit" 
            className="auth-btn"
            disabled={loading}
            style={{
              opacity: loading ? 0.7 : 1,
              cursor: loading ? 'not-allowed' : 'pointer',
              position: 'relative'
            }}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Creating Account...
              </>
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        <div className="auth-footer">
          <p>Already have an account?</p>
          <button onClick={switchToLogin} className="auth-link">
            Back to Login
          </button>
        </div>
      </div>

      {/* Add these styles */}
      <style jsx>{`
        .custom-alert {
          display: flex;
          align-items: flex-start;
          padding: 16px;
          border-radius: 12px;
          margin-bottom: 20px;
          animation: slideIn 0.3s ease;
          position: relative;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .alert-error {
          background: linear-gradient(135deg, #fee2e2 0%, #ffefef 100%);
          border-left: 4px solid #ef4444;
        }

        .alert-success {
          background: linear-gradient(135deg, #dcfce7 0%, #f0fdf4 100%);
          border-left: 4px solid #22c55e;
        }

        .alert-icon {
          font-size: 24px;
          margin-right: 12px;
          line-height: 1;
        }

        .alert-content {
          flex: 1;
        }

        .alert-title {
          font-weight: 700;
          font-size: 14px;
          margin-bottom: 4px;
        }

        .alert-error .alert-title {
          color: #991b1b;
        }

        .alert-success .alert-title {
          color: #166534;
        }

        .alert-message {
          font-size: 13px;
          color: #4b5563;
          line-height: 1.4;
        }

        .alert-close {
          background: none;
          border: none;
          font-size: 20px;
          cursor: pointer;
          color: #9ca3af;
          padding: 0 4px;
          transition: color 0.2s;
        }

        .alert-close:hover {
          color: #4b5563;
        }

        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateX(20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        .spinner {
          display: inline-block;
          width: 16px;
          height: 16px;
          border: 2px solid rgba(255,255,255,0.3);
          border-radius: 50%;
          border-top-color: white;
          animation: spin 0.8s linear infinite;
          margin-right: 8px;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default Signup;