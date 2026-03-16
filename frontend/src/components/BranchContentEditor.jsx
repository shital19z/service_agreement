// frontend/src/components/BranchContentEditor.jsx
import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';

const BranchContentEditor = ({ isOpen, onClose, onSave, token, branchCode, branchName }) => {
    const [content, setContent] = useState({});
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [activeTab, setActiveTab] = useState('page1');
    const [saveSuccess, setSaveSuccess] = useState(false);

    useEffect(() => {
        if (isOpen && branchCode) {
            fetchContent();
            setSaveSuccess(false);
        }
    }, [isOpen, branchCode]);

    const fetchContent = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${endpoint}/branches/${branchCode}/content`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            setContent(data);
        } catch (error) {
            console.error('Error fetching content:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setContent(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSave = async () => {
        setSaving(true);
        setSaveSuccess(false);
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
                setSaveSuccess(true);
                setTimeout(() => {
                    alert('✅ Template saved successfully! This content will now auto-populate new agreements for this branch.');
                    onSave();
                    onClose();
                }, 500);
            } else {
                alert('❌ Failed to save content');
            }
        } catch (error) {
            console.error('Error saving content:', error);
            alert('❌ Error saving content');
        } finally {
            setSaving(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '900px', width: '95%', maxHeight: '90vh' }}>
                <div className="modal-header">
                    <h3>
                        <span style={{ marginRight: '8px' }}>📋</span>
                        Edit Branch Template: {branchName}
                    </h3>
                    <button className="modal-close" onClick={onClose}>×</button>
                </div>

                {/* Info Banner */}
                <div style={{
                    background: 'linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%)',
                    borderLeft: '4px solid #4facfe',
                    padding: '12px 20px',
                    margin: '0 20px 10px 20px',
                    borderRadius: '8px',
                    fontSize: '13px',
                    color: '#0369a1',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px'
                }}>
                    <span style={{ fontSize: '20px' }}>ℹ️</span>
                    <span>
                        <strong>Template Content:</strong> This content will auto-populate new agreements when this branch is selected. 
                        Fields marked with <span style={{ color: '#4facfe', fontWeight: 'bold' }}>✨</span> directly affect agreement generation.
                    </span>
                </div>

                <div className="modal-body" style={{ maxHeight: 'calc(90vh - 160px)', overflowY: 'auto', padding: '20px' }}>
                    {/* Tab Navigation */}
                    <div style={{ display: 'flex', borderBottom: '2px solid #e2e8f0', marginBottom: '20px', flexWrap: 'wrap' }}>
                        <TabButton active={activeTab === 'page1'} onClick={() => setActiveTab('page1')}>
                            Page 1 <span style={{ fontSize: '10px', marginLeft: '5px', color: '#4facfe' }}>✨</span>
                        </TabButton>
                        <TabButton active={activeTab === 'page1cont'} onClick={() => setActiveTab('page1cont')}>
                            Page 1 Cont <span style={{ fontSize: '10px', marginLeft: '5px', color: '#4facfe' }}>✨</span>
                        </TabButton>
                        <TabButton active={activeTab === 'page2'} onClick={() => setActiveTab('page2')}>
                            Page 2 <span style={{ fontSize: '10px', marginLeft: '5px', color: '#4facfe' }}>✨</span>
                        </TabButton>
                        <TabButton active={activeTab === 'page3'} onClick={() => setActiveTab('page3')}>
                            Page 3 <span style={{ fontSize: '10px', marginLeft: '5px', color: '#4facfe' }}>✨</span>
                        </TabButton>
                        <TabButton active={activeTab === 'settings'} onClick={() => setActiveTab('settings')}>
                            Settings
                        </TabButton>
                    </div>

                    {loading ? (
                        <div style={{ textAlign: 'center', padding: '40px' }}>
                            <div style={{ 
                                width: '40px', 
                                height: '40px', 
                                border: '3px solid #e2e8f0',
                                borderTopColor: '#4facfe',
                                borderRadius: '50%',
                                animation: 'spin 1s linear infinite',
                                margin: '0 auto 15px auto'
                            }}></div>
                            Loading template content...
                        </div>
                    ) : (
                        <>
                            {/* PAGE 1 TAB */}
                            {activeTab === 'page1' && (
                                <div>
                                    <h4 style={{ marginBottom: '15px', color: '#0f172a' }}>
                                        Page 1 - Main Agreement 
                                        <span style={{ fontSize: '12px', fontWeight: 'normal', marginLeft: '10px', color: '#64748b' }}>
                                            (These fields auto-fill in new agreements)
                                        </span>
                                    </h4>
                                    
                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Required Services Introduction
                                        </label>
                                        <textarea
                                            name="required_services"
                                            value={content.required_services || ''}
                                            onChange={handleChange}
                                            rows="4"
                                            className="form-input"
                                            placeholder="Enter the required services introduction text..."
                                        />
                                        <small style={{ color: '#64748b' }}>This text appears in the REQUIRED SERVICES section</small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Frequency of Visits (placeholder)
                                        </label>
                                        <input
                                            type="text"
                                            name="freq_of_visit"
                                            value={content.freq_of_visit || ''}
                                            onChange={handleChange}
                                            className="form-input"
                                            placeholder="e.g., Daily, Weekly, Mon-Fri"
                                        />
                                        <small style={{ color: '#64748b' }}>Default text for FREQUENCY DURATION OF VISITS</small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Hazards (placeholder)
                                        </label>
                                        <input
                                            type="text"
                                            name="hazards"
                                            value={content.hazards || ''}
                                            onChange={handleChange}
                                            className="form-input"
                                            placeholder="None Reported"
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label>Care Type</label>
                                        <input
                                            type="text"
                                            name="care_type"
                                            value={content.care_type || 'Home Care'}
                                            onChange={handleChange}
                                            className="form-input"
                                        />
                                    </div>

                                    <div className="form-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
                                        <div className="form-group">
                                            <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                                <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                                Hourly Rate ($)
                                            </label>
                                            <input
                                                type="number"
                                                name="hourly_rate"
                                                value={content.hourly_rate || 36.00}
                                                onChange={handleChange}
                                                step="0.01"
                                                className="form-input"
                                            />
                                        </div>

                                        <div className="form-group">
                                            <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                                <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                                Mileage Rate ($/mile)
                                            </label>
                                            <input
                                                type="number"
                                                name="mileage_rate"
                                                value={content.mileage_rate || 0.67}
                                                onChange={handleChange}
                                                step="0.01"
                                                className="form-input"
                                            />
                                        </div>
                                    </div>

                                    <div className="form-group">
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Percentage Charged (%)
                                        </label>
                                        <input
                                            type="number"
                                            name="perc_charged"
                                            value={content.perc_charged || '100'}
                                            onChange={handleChange}
                                            min="0"
                                            max="100"
                                            className="form-input"
                                        />
                                    </div>
                                </div>
                            )}

                            {/* PAGE 1 CONT TAB */}
                            {activeTab === 'page1cont' && (
                                <div>
                                    <h4 style={{ marginBottom: '15px', color: '#0f172a' }}>
                                        Page 1 Continuation - Additional Terms
                                        <span style={{ fontSize: '12px', fontWeight: 'normal', marginLeft: '10px', color: '#64748b' }}>
                                            (These fields auto-fill in new agreements)
                                        </span>
                                    </h4>
                                    
                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Notice Period Text
                                        </label>
                                        <textarea
                                            name="notice_period_text"
                                            value={content.notice_period_text || ''}
                                            onChange={handleChange}
                                            rows="4"
                                            className="form-input"
                                            placeholder="e.g. OPTIONS may end services by giving 3 calendar days notice in writing..."
                                        />
                                        <small style={{ color: '#64748b' }}>Leave blank to use the default for this branch type (3-day or 10-day)</small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Needs Assessment & Plan of Care
                                        </label>
                                        <textarea
                                            name="needs_assessment_text"
                                            value={content.needs_assessment_text || ''}
                                            onChange={handleChange}
                                            rows="3"
                                            className="form-input"
                                            placeholder="Enter needs assessment text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Your Valuables
                                        </label>
                                        <textarea
                                            name="valuables_text"
                                            value={content.valuables_text || ''}
                                            onChange={handleChange}
                                            rows="3"
                                            className="form-input"
                                            placeholder="Enter valuables text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Medication Administration
                                        </label>
                                        <textarea
                                            name="medication_text"
                                            value={content.medication_text || ''}
                                            onChange={handleChange}
                                            rows="3"
                                            className="form-input"
                                            placeholder="Enter medication text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Cannot Be Hired
                                        </label>
                                        <textarea
                                            name="cannot_hire_text"
                                            value={content.cannot_hire_text || ''}
                                            onChange={handleChange}
                                            rows="6"
                                            className="form-input"
                                            placeholder="Enter cannot be hired text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Record Keeping
                                        </label>
                                        <textarea
                                            name="record_keeping_text"
                                            value={content.record_keeping_text || ''}
                                            onChange={handleChange}
                                            rows="4"
                                            className="form-input"
                                            placeholder="Enter record keeping text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Mileage Reimbursement
                                        </label>
                                        <textarea
                                            name="mileage_reimbursement_text"
                                            value={content.mileage_reimbursement_text || ''}
                                            onChange={handleChange}
                                            rows="3"
                                            className="form-input"
                                            placeholder="Enter mileage reimbursement text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Use of Family Vehicle
                                        </label>
                                        <textarea
                                            name="vehicle_use_text"
                                            value={content.vehicle_use_text || ''}
                                            onChange={handleChange}
                                            rows="2"
                                            className="form-input"
                                            placeholder="Enter vehicle use text..."
                                        />
                                    </div>
                                </div>
                            )}

                            {/* PAGE 2 TAB */}
                            {activeTab === 'page2' && (
                                <div>
                                    <h4 style={{ marginBottom: '15px', color: '#0f172a' }}>
                                        Page 2 - Patient Rights & Billing
                                        <span style={{ fontSize: '12px', fontWeight: 'normal', marginLeft: '10px', color: '#64748b' }}>
                                            (These fields auto-fill in new agreements)
                                        </span>
                                    </h4>
                                    
                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Patients' Rights Text
                                        </label>
                                        <textarea
                                            name="patients_rights_text"
                                            value={content.patients_rights_text || ''}
                                            onChange={handleChange}
                                            rows="12"
                                            className="form-input"
                                            placeholder="Enter patients' rights text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Complaint Procedures Text
                                        </label>
                                        <textarea
                                            name="complaint_procedures_text"
                                            value={content.complaint_procedures_text || ''}
                                            onChange={handleChange}
                                            rows="10"
                                            className="form-input"
                                            placeholder="Enter complaint procedures text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Billing Procedures Text
                                        </label>
                                        <textarea
                                            name="billing_procedures_text"
                                            value={content.billing_procedures_text || ''}
                                            onChange={handleChange}
                                            rows="12"
                                            className="form-input"
                                            placeholder="Enter billing procedures text..."
                                        />
                                    </div>
                                </div>
                            )}

                            {/* PAGE 3 TAB */}
                            {activeTab === 'page3' && (
                                <div>
                                    <h4 style={{ marginBottom: '15px', color: '#0f172a' }}>
                                        Page 3 - EFT Authorization
                                        <span style={{ fontSize: '12px', fontWeight: 'normal', marginLeft: '10px', color: '#64748b' }}>
                                            (These fields auto-fill in new agreements)
                                        </span>
                                    </h4>
                                    
                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            EFT Authorization Text
                                        </label>
                                        <textarea
                                            name="eft_authorization_text"
                                            value={content.eft_authorization_text || ''}
                                            onChange={handleChange}
                                            rows="15"
                                            className="form-input"
                                            placeholder="Enter EFT authorization text..."
                                        />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                            <span style={{ color: '#4facfe', fontSize: '16px' }}>✨</span>
                                            Consumer Notice Text (Page 3.1)
                                        </label>
                                        <textarea
                                            name="consumer_notice_text"
                                            value={content.consumer_notice_text || ''}
                                            onChange={handleChange}
                                            rows="8"
                                            className="form-input"
                                            placeholder="Enter consumer notice text..."
                                        />
                                    </div>
                                </div>
                            )}

                            {/* SETTINGS TAB */}
                            {activeTab === 'settings' && (
                                <div>
                                    <h4 style={{ marginBottom: '15px', color: '#0f172a' }}>
                                        Branch Settings
                                        <span style={{ fontSize: '12px', fontWeight: 'normal', marginLeft: '10px', color: '#64748b' }}>
                                            (These affect validation and behavior)
                                        </span>
                                    </h4>
                                    
                                    <div className="form-group" style={{ marginBottom: '20px', background: '#f8fafc', padding: '15px', borderRadius: '8px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                                            <input
                                                type="checkbox"
                                                name="has_initial_contact"
                                                checked={content.has_initial_contact || false}
                                                onChange={handleChange}
                                                style={{ width: '18px', height: '18px' }}
                                            />
                                            <span style={{ fontWeight: 'bold' }}>Requires Initial Contact Date</span>
                                        </label>
                                        <small style={{ color: '#64748b', display: 'block', marginTop: '5px', marginLeft: '28px' }}>
                                            When checked, the Initial Contact Date field becomes required in the agreement form (for GA/SC branches)
                                        </small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px', background: '#f8fafc', padding: '15px', borderRadius: '8px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                                            <input
                                                type="checkbox"
                                                name="requires_consumer_notice"
                                                checked={content.requires_consumer_notice || false}
                                                onChange={handleChange}
                                                style={{ width: '18px', height: '18px' }}
                                            />
                                            <span style={{ fontWeight: 'bold' }}>Requires Consumer Notice Page (Page 3.1)</span>
                                        </label>
                                        <small style={{ color: '#64748b', display: 'block', marginTop: '5px', marginLeft: '28px' }}>
                                            When checked, the Consumer Notice of Direct Care Worker Status page is added to the PDF (PA branches)
                                        </small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label>Holiday Count</label>
                                        <select
                                            name="holiday_count"
                                            value={content.holiday_count || 11}
                                            onChange={handleChange}
                                            className="form-input"
                                        >
                                            <option value="11">11 Holidays (Standard)</option>
                                            <option value="12">12 Holidays (Includes Easter Sunday)</option>
                                        </select>
                                        <small style={{ color: '#64748b' }}>Affects the Federal Holidays section in the agreement</small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label>Special Instructions</label>
                                        <textarea
                                            name="special_instructions"
                                            value={content.special_instructions || ''}
                                            onChange={handleChange}
                                            rows="2"
                                            className="form-input"
                                            placeholder="Any special instructions for this branch..."
                                        />
                                        <small style={{ color: '#64748b' }}>Internal notes only - not shown in agreements</small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label>Default Care Type</label>
                                        <input
                                            type="text"
                                            name="care_type"
                                            value={content.care_type || 'Home Care'}
                                            onChange={handleChange}
                                            className="form-input"
                                        />
                                    </div>
                                </div>
                            )}

                            {/* Quick Tips Section */}
                            <div style={{
                                marginTop: '30px',
                                padding: '15px',
                                background: '#f1f5f9',
                                borderRadius: '8px',
                                border: '1px dashed #94a3b8'
                            }}>
                                <h5 style={{ margin: '0 0 10px 0', color: '#0f172a', fontSize: '14px' }}>
                                    📝 Template Tips:
                                </h5>
                                <ul style={{ margin: 0, paddingLeft: '20px', color: '#334155', fontSize: '12px' }}>
                                    <li>Fields marked with <span style={{ color: '#4facfe' }}>✨</span> will auto-populate new agreements</li>
                                    <li>Save this template to set defaults for all future agreements using {branchName}</li>
                                    <li>Users can still override these values when creating individual agreements</li>
                                    <li>Settings tab controls validation rules and branch behavior</li>
                                </ul>
                            </div>
                        </>
                    )}
                </div>

                <div className="modal-footer" style={{ 
                    padding: '20px', 
                    borderTop: '1px solid #e2e8f0', 
                    display: 'flex', 
                    gap: '10px', 
                    justifyContent: 'flex-end',
                    background: '#f8fafc'
                }}>
                    {saveSuccess && (
                        <div style={{ 
                            color: '#10b981', 
                            fontSize: '14px', 
                            display: 'flex', 
                            alignItems: 'center',
                            marginRight: 'auto'
                        }}>
                            ✓ Saved successfully!
                        </div>
                    )}
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                    <button 
                        className="action-btn" 
                        onClick={handleSave} 
                        disabled={saving}
                        style={{
                            background: saving ? '#94a3b8' : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                            minWidth: '120px'
                        }}
                    >
                        {saving ? 'Saving...' : '💾 Save Template'}
                    </button>
                </div>
            </div>
            <style>{`
                @keyframes spin {
                    to { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
};

const TabButton = ({ active, onClick, children }) => (
    <button
        onClick={onClick}
        style={{
            padding: '10px 20px',
            background: active ? '#4facfe' : 'transparent',
            color: active ? 'white' : '#64748b',
            border: 'none',
            borderBottom: active ? '3px solid #2563eb' : 'none',
            cursor: 'pointer',
            fontWeight: active ? '600' : '400',
            fontSize: '14px',
            transition: 'all 0.2s'
        }}
        onMouseOver={(e) => {
            if (!active) {
                e.target.style.background = '#f1f5f9';
                e.target.style.color = '#0f172a';
            }
        }}
        onMouseOut={(e) => {
            if (!active) {
                e.target.style.background = 'transparent';
                e.target.style.color = '#64748b';
            }
        }}
    >
        {children}
    </button>
);

export default BranchContentEditor;