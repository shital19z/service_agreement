import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';
import './SharedAgreementView.css';

const SharedAgreementView = () => {
    const [agreement, setAgreement] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [pdfUrl, setPdfUrl] = useState(null);

    useEffect(() => {
        // Get token from URL
        const pathParts = window.location.pathname.split('/');
        const token = pathParts[pathParts.length - 1];
        
        if (!token) {
            setError('Invalid share link');
            setLoading(false);
            return;
        }

        // Fetch agreement details
        fetchAgreement(token);
    }, []);

    const fetchAgreement = async (token) => {
        try {
            const response = await fetch(`${endpoint}/shared-agreement/${token}`);
            
            if (!response.ok) {
                throw new Error('Agreement not found or link expired');
            }
            
            const data = await response.json();
            setAgreement(data);
            
            // Also fetch the PDF
            fetchPDF(token);
            
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    const fetchPDF = async (token) => {
        try {
            const response = await fetch(`${endpoint}/shared-agreement/${token}/pdf`);
            
            if (!response.ok) {
                throw new Error('Failed to load PDF');
            }
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            setPdfUrl(url);
            
        } catch (err) {
            console.error('PDF load error:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="shared-loading">
                <div className="loading-spinner"></div>
                <p>Loading agreement...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="shared-error">
                <h2>⚠️ Error</h2>
                <p>{error}</p>
                <p>The link may have expired or is invalid.</p>
            </div>
        );
    }

    return (
        <div className="shared-container">
            <div className="shared-header">
                <h1>Service Agreement</h1>
                {agreement && (
                    <div className="agreement-info">
                        <p><strong>Client:</strong> {agreement.clt_first_name} {agreement.clt_last_name}</p>
                        <p><strong>Branch:</strong> {agreement.branch_code}</p>
                        <p><strong>Rate:</strong> ${agreement.hourly_rate}/hr</p>
                    </div>
                )}
            </div>
            
            <div className="pdf-viewer">
                {pdfUrl ? (
                    <iframe 
                        src={pdfUrl} 
                        className="pdf-iframe"
                        title="Agreement PDF"
                    />
                ) : (
                    <div className="pdf-loading">Loading PDF...</div>
                )}
            </div>
            
            <div className="shared-footer">
                <p>This link will expire in 7 days</p>
            </div>
        </div>
    );
};

export default SharedAgreementView;