import React, { useState } from 'react';
import { endpoint } from '../resource/Constant';

const ShareModal = ({ isOpen, onClose, agreementId, agreementName, token }) => {
    const [email, setEmail] = useState('');
    const [sending, setSending] = useState(false);
    const [message, setMessage] = useState('');
    const [shareLink, setShareLink] = useState('');

    const generateShareLink = async () => {
        try {
            // Create a shareable link (you'll need a backend endpoint for this)
            const response = await fetch(`${endpoint}/agreements/${agreementId}/share-link`, {
                method: 'POST',
                headers: { 
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) throw new Error('Failed to generate link');
            
            const data = await response.json();
            setShareLink(data.share_link);
            
        } catch (err) {
            console.error('Error generating share link:', err);
            setMessage('Failed to generate share link');
        }
    };

    const sendEmail = async (e) => {
        e.preventDefault();
        setSending(true);
        setMessage('');

        try {
            const response = await fetch(`${endpoint}/agreements/${agreementId}/share-email`, {
                method: 'POST',
                headers: { 
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            if (!response.ok) throw new Error('Failed to send email');

            setMessage('Email sent successfully!');
            setEmail('');
            setTimeout(() => {
                onClose();
                setMessage('');
            }, 2000);
            
        } catch (err) {
            console.error('Error sending email:', err);
            setMessage('Failed to send email');
        } finally {
            setSending(false);
        }
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(shareLink);
        setMessage('Link copied to clipboard!');
        setTimeout(() => setMessage(''), 3000);
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <div className="modal-header">
                    <h3>Share Agreement: {agreementName}</h3>
                    <button className="modal-close" onClick={onClose}>×</button>
                </div>

                <div className="modal-body">
                    {message && (
                        <div className={`message-banner ${message.includes('success') ? 'success' : 'error'}`}>
                            {message}
                        </div>
                    )}

                    {/* Share Link Section */}
                    <div className="share-section">
                        <h4>Shareable Link</h4>
                        {!shareLink ? (
                            <button 
                                onClick={generateShareLink} 
                                className="generate-link-btn"
                            >
                                Generate Share Link
                            </button>
                        ) : (
                            <div className="link-container">
                                <input 
                                    type="text" 
                                    value={shareLink} 
                                    readOnly 
                                    className="share-link-input"
                                />
                                <button 
                                    onClick={copyToClipboard} 
                                    className="copy-btn"
                                >
                                    Copy
                                </button>
                            </div>
                        )}
                    </div>

                    <div className="divider">OR</div>

                    {/* Email Share Section */}
                    <div className="share-section">
                        <h4>Share via Email</h4>
                        <form onSubmit={sendEmail}>
                            <input
                                type="email"
                                placeholder="Enter email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="email-input"
                            />
                            <button 
                                type="submit" 
                                disabled={sending}
                                className="send-email-btn"
                            >
                                {sending ? 'Sending...' : 'Send Email'}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ShareModal;