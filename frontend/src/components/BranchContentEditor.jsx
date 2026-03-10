import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';

const BranchContentEditor = ({ isOpen, onClose, onSave, token, branchCode, branchName }) => {
    const [activeTab, setActiveTab] = useState('page1');
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    
    const [content, setContent] = useState({
        // Page 1
        required_services: '',
        freq_of_visit: '',
        hazards: '',
        charges_text: '',
        payment_obligations_text: '',
        live_in_text: '',
        holiday_count: 11,
        holidays_list: [],
        
        // Page 1 Cont
        needs_assessment_text: '',
        valuables_text: '',
        notice_period_text: '',
        cannot_hire_text: '',
        record_keeping_text: '',
        mileage_reimbursement_text: '',
        vehicle_use_text: '',
        general_provisions: [],
        
        // Page 2
        patients_rights_text: '',
        complaint_procedures_text: '',
        billing_procedures_text: '',
        
        // Page 3
        eft_authorization_text: '',
        
        // Settings
        has_initial_contact: false,
        requires_consumer_notice: false,
        care_type: 'Home Care',
        mileage_rate: 0.67,
        hourly_rate: 36.00,
        perc_charged: '100'
    });

    useEffect(() => {
        if (isOpen && branchCode) {
            fetchContent();
        }
    }, [isOpen, branchCode]);

    const fetchContent = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${endpoint}/branches/${branchCode}/content`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            setContent(prev => ({ ...prev, ...data }));
        } catch (err) {
            setError('Failed to load content');
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        setSaving(true);
        setError('');
        setSuccess('');
        
        try {
            const response = await fetch(`${endpoint}/branches/${branchCode}/content`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(content)
            });
            
            if (response.ok) {
                setSuccess('Content saved successfully!');
                setTimeout(() => {
                    onSave();
                    onClose();
                }, 1500);
            } else {
                const data = await response.json();
                setError(data.detail || 'Failed to save');
            }
        } catch (err) {
            setError('Failed to connect to server');
        } finally {
            setSaving(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '900px', maxHeight: '90vh', overflow: 'hidden' }}>
                <div className="modal-header">
                    <h3>Edit Content: {branchName}</h3>
                    <button onClick={onClose} className="modal-close">×</button>
                </div>

                {loading ? (
                    <div style={{ padding: '40px', textAlign: 'center' }}>Loading...</div>
                ) : (
                    <>
                        {/* Tab Navigation */}
                        <div style={{ 
                            display: 'flex', 
                            gap: '2px', 
                            padding: '0 20px',
                            borderBottom: '2px solid #e2e8f0',
                            background: '#f8fafc'
                        }}>
                            <TabButton 
                                active={activeTab === 'page1'} 
                                onClick={() => setActiveTab('page1')}
                            >
                                Page 1
                            </TabButton>
                            <TabButton 
                                active={activeTab === 'page1cont'} 
                                onClick={() => setActiveTab('page1cont')}
                            >
                                Page 1 Cont
                            </TabButton>
                            <TabButton 
                                active={activeTab === 'page2'} 
                                onClick={() => setActiveTab('page2')}
                            >
                                Page 2 - Rights
                            </TabButton>
                            <TabButton 
                                active={activeTab === 'page3'} 
                                onClick={() => setActiveTab('page3')}
                            >
                                Page 3 - EFT
                            </TabButton>
                            <TabButton 
                                active={activeTab === 'settings'} 
                                onClick={() => setActiveTab('settings')}
                            >
                                Settings
                            </TabButton>
                        </div>

                        {/* Scrollable Content Area */}
                        <div style={{ 
                            padding: '20px', 
                            maxHeight: 'calc(90vh - 180px)', 
                            overflowY: 'auto' 
                        }}>
                            {error && (
                                <div style={{ 
                                    background: '#fee2e2', 
                                    color: '#991b1b',
                                    padding: '12px',
                                    borderRadius: '6px',
                                    marginBottom: '20px'
                                }}>
                                    {error}
                                </div>
                            )}
                            
                            {success && (
                                <div style={{ 
                                    background: '#dcfce7', 
                                    color: '#166534',
                                    padding: '12px',
                                    borderRadius: '6px',
                                    marginBottom: '20px'
                                }}>
                                    {success}
                                </div>
                            )}

                            {/* Page 1 Content */}
                            {activeTab === 'page1' && (
                                <div>
                                    <h4 style={{ marginBottom: '20px' }}>Page 1 - Service Agreement</h4>
                                    
                                    <Section label="Required Services">
                                        <textarea
                                            value={content.required_services}
                                            onChange={(e) => setContent({...content, required_services: e.target.value})}
                                            rows={4}
                                            style={textareaStyle}
                                            placeholder="Enter required services description..."
                                        />
                                    </Section>

                                    <Section label="Frequency of Visits">
                                        <input
                                            type="text"
                                            value={content.freq_of_visit}
                                            onChange={(e) => setContent({...content, freq_of_visit: e.target.value})}
                                            style={inputStyle}
                                            placeholder="e.g., Daily, Weekly, Mon-Fri"
                                        />
                                    </Section>

                                    <Section label="Hazards">
                                        <textarea
                                            value={content.hazards}
                                            onChange={(e) => setContent({...content, hazards: e.target.value})}
                                            rows={2}
                                            style={textareaStyle}
                                            placeholder="None Reported"
                                        />
                                    </Section>

                                    <Section label="Charges Text">
                                        <textarea
                                            value={content.charges_text}
                                            onChange={(e) => setContent({...content, charges_text: e.target.value})}
                                            rows={3}
                                            style={textareaStyle}
                                            placeholder="We bill bi-weekly for services rendered..."
                                        />
                                    </Section>

                                    <Section label="Payment Obligations">
                                        <textarea
                                            value={content.payment_obligations_text}
                                            onChange={(e) => setContent({...content, payment_obligations_text: e.target.value})}
                                            rows={3}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Live-in Services Text">
                                        <textarea
                                            value={content.live_in_text}
                                            onChange={(e) => setContent({...content, live_in_text: e.target.value})}
                                            rows={4}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Holiday Count">
                                        <input
                                            type="number"
                                            value={content.holiday_count}
                                            onChange={(e) => setContent({...content, holiday_count: parseInt(e.target.value)})}
                                            style={{...inputStyle, width: '100px'}}
                                            min="0"
                                            max="15"
                                        />
                                    </Section>
                                </div>
                            )}

                            {/* Page 1 Cont Content */}
                            {activeTab === 'page1cont' && (
                                <div>
                                    <h4 style={{ marginBottom: '20px' }}>Page 1 - Continuation</h4>
                                    
                                    <Section label="Needs Assessment Text">
                                        <textarea
                                            value={content.needs_assessment_text}
                                            onChange={(e) => setContent({...content, needs_assessment_text: e.target.value})}
                                            rows={3}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Valuables Text">
                                        <textarea
                                            value={content.valuables_text}
                                            onChange={(e) => setContent({...content, valuables_text: e.target.value})}
                                            rows={3}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Notice Period Text">
                                        <textarea
                                            value={content.notice_period_text}
                                            onChange={(e) => setContent({...content, notice_period_text: e.target.value})}
                                            rows={3}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Cannot Hire Text">
                                        <textarea
                                            value={content.cannot_hire_text}
                                            onChange={(e) => setContent({...content, cannot_hire_text: e.target.value})}
                                            rows={4}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Record Keeping Text">
                                        <textarea
                                            value={content.record_keeping_text}
                                            onChange={(e) => setContent({...content, record_keeping_text: e.target.value})}
                                            rows={4}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Mileage Reimbursement Text">
                                        <textarea
                                            value={content.mileage_reimbursement_text}
                                            onChange={(e) => setContent({...content, mileage_reimbursement_text: e.target.value})}
                                            rows={3}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Vehicle Use Text">
                                        <textarea
                                            value={content.vehicle_use_text}
                                            onChange={(e) => setContent({...content, vehicle_use_text: e.target.value})}
                                            rows={2}
                                            style={textareaStyle}
                                        />
                                    </Section>
                                </div>
                            )}

                            {/* Page 2 Content */}
                            {activeTab === 'page2' && (
                                <div>
                                    <h4 style={{ marginBottom: '20px' }}>Page 2 - Patient Rights & Procedures</h4>
                                    
                                    <Section label="Patients Rights Text">
                                        <textarea
                                            value={content.patients_rights_text}
                                            onChange={(e) => setContent({...content, patients_rights_text: e.target.value})}
                                            rows={6}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Complaint Procedures Text">
                                        <textarea
                                            value={content.complaint_procedures_text}
                                            onChange={(e) => setContent({...content, complaint_procedures_text: e.target.value})}
                                            rows={6}
                                            style={textareaStyle}
                                        />
                                    </Section>

                                    <Section label="Billing Procedures Text">
                                        <textarea
                                            value={content.billing_procedures_text}
                                            onChange={(e) => setContent({...content, billing_procedures_text: e.target.value})}
                                            rows={6}
                                            style={textareaStyle}
                                        />
                                    </Section>
                                </div>
                            )}

                            {/* Page 3 Content */}
                            {activeTab === 'page3' && (
                                <div>
                                    <h4 style={{ marginBottom: '20px' }}>Page 3 - EFT Authorization</h4>
                                    
                                    <Section label="EFT Authorization Text">
                                        <textarea
                                            value={content.eft_authorization_text}
                                            onChange={(e) => setContent({...content, eft_authorization_text: e.target.value})}
                                            rows={6}
                                            style={textareaStyle}
                                        />
                                    </Section>
                                </div>
                            )}

                            {/* Settings Tab */}
                            {activeTab === 'settings' && (
                                <div>
                                    <h4 style={{ marginBottom: '20px' }}>Branch Settings</h4>
                                    
                                    <div style={gridStyle}>
                                        <Section label="Hourly Rate ($)">
                                            <input
                                                type="number"
                                                value={content.hourly_rate}
                                                onChange={(e) => setContent({...content, hourly_rate: parseFloat(e.target.value)})}
                                                style={inputStyle}
                                                step="0.01"
                                                min="0"
                                            />
                                        </Section>

                                        <Section label="Mileage Rate ($)">
                                            <input
                                                type="number"
                                                value={content.mileage_rate}
                                                onChange={(e) => setContent({...content, mileage_rate: parseFloat(e.target.value)})}
                                                style={inputStyle}
                                                step="0.01"
                                                min="0"
                                            />
                                        </Section>

                                        <Section label="Percentage Charged (%)">
                                            <input
                                                type="number"
                                                value={content.perc_charged}
                                                onChange={(e) => setContent({...content, perc_charged: e.target.value})}
                                                style={inputStyle}
                                                min="0"
                                                max="100"
                                            />
                                        </Section>

                                        <Section label="Care Type">
                                            <input
                                                type="text"
                                                value={content.care_type}
                                                onChange={(e) => setContent({...content, care_type: e.target.value})}
                                                style={inputStyle}
                                            />
                                        </Section>
                                    </div>

                                    <div style={{ marginTop: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                            <input
                                                type="checkbox"
                                                checked={content.has_initial_contact}
                                                onChange={(e) => setContent({...content, has_initial_contact: e.target.checked})}
                                            />
                                            <span>Has Initial Contact Date (GA/SC branches)</span>
                                        </label>

                                        <label style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px' }}>
                                            <input
                                                type="checkbox"
                                                checked={content.requires_consumer_notice}
                                                onChange={(e) => setContent({...content, requires_consumer_notice: e.target.checked})}
                                            />
                                            <span>Requires Consumer Notice (PA branches)</span>
                                        </label>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Footer */}
                        <div style={{ 
                            padding: '20px',
                            borderTop: '1px solid #e2e8f0',
                            display: 'flex',
                            gap: '10px',
                            justifyContent: 'flex-end'
                        }}>
                            <button onClick={onClose} className="cancel-btn">
                                Cancel
                            </button>
                            <button 
                                onClick={handleSave} 
                                className="action-btn"
                                disabled={saving}
                            >
                                {saving ? 'Saving...' : 'Save Content'}
                            </button>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

// Helper Components
const TabButton = ({ active, onClick, children }) => (
    <button
        onClick={onClick}
        style={{
            padding: '12px 20px',
            background: active ? '#4facfe' : 'transparent',
            color: active ? 'white' : '#64748b',
            border: 'none',
            borderBottom: active ? '2px solid #4facfe' : '2px solid transparent',
            cursor: 'pointer',
            fontWeight: active ? '600' : '400',
            transition: 'all 0.2s'
        }}
    >
        {children}
    </button>
);

const Section = ({ label, children }) => (
    <div style={{ marginBottom: '20px' }}>
        <label style={{ 
            fontWeight: '600', 
            display: 'block', 
            marginBottom: '5px',
            color: '#1e293b'
        }}>
            {label}
        </label>
        {children}
    </div>
);

const inputStyle = {
    width: '100%',
    padding: '10px',
    border: '2px solid #e2e8f0',
    borderRadius: '6px',
    fontSize: '14px'
};

const textareaStyle = {
    ...inputStyle,
    resize: 'vertical'
};

const gridStyle = {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '20px'
};

export default BranchContentEditor;