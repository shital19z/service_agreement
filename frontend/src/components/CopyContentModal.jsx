import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';

const CopyContentModal = ({ isOpen, onClose, onCopy, token, currentBranchCode, branchName }) => {
    const [branches, setBranches] = useState([]);
    const [selectedSource, setSelectedSource] = useState('');
    const [contentTypes, setContentTypes] = useState({
        agreements: true,
        rates: true,
        services: true
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (isOpen) {
            fetchBranches();
        }
    }, [isOpen]);

    const fetchBranches = async () => {
        try {
            const response = await fetch(`${endpoint}/branches?t=${new Date().getTime()}`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            // Filter out current branch so user can't copy from itself
            setBranches(data.filter(b => b.branch_code !== currentBranchCode));
        } catch (err) {
            console.error('Error fetching branches:', err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedSource) {
            setError('Please select a source branch');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const response = await fetch(`${endpoint}/branches/copy-content`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source_branch: selectedSource,
                    target_branches: [currentBranchCode],
                    content_types: contentTypes
                })
            });

            if (!response.ok) {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to copy content');
            }

            const data = await response.json();
            onCopy(data.results);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '500px' }}>
                <div className="modal-header">
                    <h3>Copy Content to {branchName || 'New Branch'}</h3>
                    <button className="modal-close" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="modal-body">
                        <p style={{ marginBottom: '20px', color: '#475569' }}>
                            Would you like to copy agreement content from an existing branch?
                        </p>

                        {error && (
                            <div className="message-banner error" style={{ marginBottom: '20px' }}>
                                {error}
                            </div>
                        )}

                        <div className="form-group">
                            <label style={{ fontWeight: 'bold', marginBottom: '8px', display: 'block' }}>
                                Source Branch <span style={{ color: '#ef4444' }}>*</span>
                            </label>
                            <select
                                className="form-input"
                                value={selectedSource}
                                onChange={(e) => setSelectedSource(e.target.value)}
                                required
                                style={{ width: '100%', padding: '10px' }}
                            >
                                <option value="">-- Select Source Branch --</option>
                                {branches.map(branch => (
                                    <option key={branch.branch_code} value={branch.branch_code}>
                                        {branch.branch_name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div style={{ marginTop: '20px' }}>
                            <label style={{ fontWeight: 'bold', marginBottom: '12px', display: 'block' }}>
                                What would you like to copy?
                            </label>
                            
                            <div style={{ 
                                display: 'flex', 
                                flexDirection: 'column', 
                                gap: '12px',
                                padding: '15px',
                                background: '#f8fafc',
                                borderRadius: '8px'
                            }}>
                                <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <input
                                        type="checkbox"
                                        checked={contentTypes.agreements}
                                        onChange={(e) => setContentTypes({
                                            ...contentTypes,
                                            agreements: e.target.checked
                                        })}
                                        style={{ width: '16px', height: '16px' }}
                                    />
                                    <span style={{ fontSize: '14px', color: '#1e293b' }}>
                                        <strong>Agreement Content</strong> (Required Services, Payment Obligations, Notice Period, Patient Rights, etc.)
                                    </span>
                                </label>
                                
                                <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <input
                                        type="checkbox"
                                        checked={contentTypes.rates}
                                        onChange={(e) => setContentTypes({
                                            ...contentTypes,
                                            rates: e.target.checked
                                        })}
                                        style={{ width: '16px', height: '16px' }}
                                    />
                                    <span style={{ fontSize: '14px', color: '#1e293b' }}>
                                        <strong>Rates</strong> (Hourly Rate, Mileage Rate)
                                    </span>
                                </label>
                                
                                <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    <input
                                        type="checkbox"
                                        checked={contentTypes.services}
                                        onChange={(e) => setContentTypes({
                                            ...contentTypes,
                                            services: e.target.checked
                                        })}
                                        style={{ width: '16px', height: '16px' }}
                                    />
                                    <span style={{ fontSize: '14px', color: '#1e293b' }}>
                                        <strong>Service Settings</strong> (Care Type, Holiday Count, Special Flags)
                                    </span>
                                </label>
                            </div>
                        </div>

                        <div style={{ 
                            fontSize: '13px', 
                            color: '#64748b', 
                            marginTop: '20px',
                            padding: '12px',
                            background: '#f1f5f9',
                            borderRadius: '6px',
                            borderLeft: '4px solid #4facfe'
                        }}>
                            <strong>💡 Note:</strong> This will copy content from the selected source branch to your new branch. Any existing content will be overwritten.
                        </div>
                    </div>

                    <div className="modal-footer" style={{ 
                        display: 'flex', 
                        gap: '10px', 
                        padding: '20px',
                        borderTop: '1px solid #e2e8f0'
                    }}>
                        <button 
                            type="button" 
                            onClick={onClose} 
                            className="cancel-btn"
                            style={{ flex: 1 }}
                        >
                            Skip
                        </button>
                        <button 
                            type="submit" 
                            className="action-btn"
                            style={{ flex: 2 }}
                            disabled={loading || !selectedSource}
                        >
                            {loading ? 'Copying...' : 'Copy Content'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CopyContentModal;