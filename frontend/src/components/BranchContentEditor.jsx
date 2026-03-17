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
                    alert('✅ Template saved successfully!');
                    onSave();
                    onClose();
                }, 500);
            } else {
                alert('❌ Failed to save content');
            }
        } catch (error) {
            alert('❌ Error saving content');
        } finally {
            setSaving(false);
        }
    };

    if (!isOpen) return null;

    const Field = ({ label, name, rows, placeholder, hint }) => (
        <div className="form-group" style={{ marginBottom: '20px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontWeight: '600', marginBottom: '6px' }}>
                <span style={{ color: '#4facfe', fontSize: '14px' }}>✨</span> {label}
            </label>
            {rows ? (
                <textarea name={name} value={content[name] || ''} onChange={handleChange}
                    rows={rows} className="form-input" placeholder={placeholder || ''} />
            ) : (
                <input type="text" name={name} value={content[name] || ''} onChange={handleChange}
                    className="form-input" placeholder={placeholder || ''} />
            )}
            {hint && <small style={{ color: '#64748b', display: 'block', marginTop: '4px' }}>{hint}</small>}
        </div>
    );

    const NumberField = ({ label, name, step, min, max, defaultVal, hint }) => (
        <div className="form-group" style={{ marginBottom: '20px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontWeight: '600', marginBottom: '6px' }}>
                <span style={{ color: '#4facfe', fontSize: '14px' }}>✨</span> {label}
            </label>
            <input type="number" name={name} value={content[name] ?? defaultVal}
                onChange={handleChange} step={step || '1'} min={min} max={max} className="form-input" />
            {hint && <small style={{ color: '#64748b', display: 'block', marginTop: '4px' }}>{hint}</small>}
        </div>
    );

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ maxWidth: '900px', width: '95%', maxHeight: '90vh' }}>
                <div className="modal-header">
                    <h3>📋 Edit Branch Template: {branchName}</h3>
                    <button className="modal-close" onClick={onClose}>×</button>
                </div>

                <div style={{
                    background: 'linear-gradient(135deg, #f0f9ff, #e6f7ff)',
                    borderLeft: '4px solid #4facfe',
                    padding: '10px 20px', margin: '0 20px 10px',
                    borderRadius: '8px', fontSize: '13px', color: '#0369a1'
                }}>
                    ℹ️ <strong>Template Content:</strong> Fields marked <span style={{ color: '#4facfe' }}>✨</span> are used in PDF generation for this branch.
                </div>

                <div className="modal-body" style={{ maxHeight: 'calc(90vh - 160px)', overflowY: 'auto', padding: '20px' }}>
                    {/* Tab Navigation */}
                    <div style={{ display: 'flex', borderBottom: '2px solid #e2e8f0', marginBottom: '20px', flexWrap: 'wrap' }}>
                        {['page1','page1cont','page2','settings'].map(tab => (
                            <TabButton key={tab} active={activeTab === tab} onClick={() => setActiveTab(tab)}>
                                {{ page1: 'Page 1', page1cont: 'Page 1 Cont', page2: 'Page 2', settings: 'Settings' }[tab]}
                                {tab !== 'settings' && <span style={{ fontSize: '10px', marginLeft: '4px', color: '#4facfe' }}>✨</span>}
                            </TabButton>
                        ))}
                    </div>

                    {loading ? (
                        <div style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>Loading template...</div>
                    ) : (
                        <>
                            {/* ── PAGE 1 ── */}
                            {activeTab === 'page1' && (
                                <div>
                                    <SectionTitle>Page 1 — Main Agreement</SectionTitle>

                                    <Field name="required_services" label="Required Services"
                                        rows={4} placeholder="In addition to the general services..."
                                        hint="Text for the REQUIRED SERVICES section" />

                                    <Field name="freq_of_visit" label="Frequency of Visits"
                                        placeholder="e.g. Daily, Weekly, Mon-Fri"
                                        hint="Text for FREQUENCY DURATION OF VISITS" />

                                    <Field name="hazards" label="Hazards"
                                        placeholder="None Reported" />

                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '15px', marginBottom: '20px' }}>
                                        <NumberField name="hourly_rate" label="Hourly Rate ($)" step="0.01" defaultVal={36.00} />
                                        <NumberField name="mileage_rate" label="Mileage Rate ($/mile)" step="0.01" defaultVal={0.67} />
                                        <NumberField name="perc_charged" label="% Charged" min={0} max={100} defaultVal={100} />
                                    </div>

                                    <Divider label="CHARGES / BILLING INTRO" />
                                    <Field name="charges_text" label="Charges Section Text" rows={3}
                                        placeholder="We bill bi-weekly for services rendered..."
                                        hint="Introductory text for the CHARGES section on Page 1" />

                                    <Divider label="PAYMENT OBLIGATIONS" />
                                    <Field name="payment_obligations_text" label="Payment Obligations Text" rows={4}
                                        placeholder="The parties responsible for payment include..." />

                                    <Divider label="FEDERAL HOLIDAYS" />
                                    <Field name="federal_holidays_text" label="Federal Holidays Text" rows={3}
                                        placeholder="When services are required on Federal holidays..." />

                                    <Divider label="LIVE-IN SERVICES" />
                                    <Field name="live_in_text" label="Live-In Services & Care Provider Schedule" rows={5}
                                        placeholder="OPTIONS care providers who provide live-in services..." />

                                    <Field name="care_type" label="Care Type"
                                        placeholder="Home Care" />
                                </div>
                            )}

                            {/* ── PAGE 1 CONT ── */}
                            {activeTab === 'page1cont' && (
                                <div>
                                    <SectionTitle>Page 1 Continuation — Additional Terms</SectionTitle>

                                    <Divider label="NEEDS ASSESSMENT & PLAN OF CARE" />
                                    <Field name="needs_assessment_text" label="Needs Assessment & Plan of Care" rows={3}
                                        placeholder="When a Needs Assessment and a Plan of Care is conducted..."
                                        hint="Leave blank to use branch default" />

                                    <Divider label="YOUR VALUABLES" />
                                    <Field name="valuables_text" label="Your Valuables" rows={3}
                                        placeholder="Our care providers are not authorized to accept payments..." />

                                    <Divider label="NOTICE PERIOD" />
                                    <Field name="notice_period_text" label="Notice Period" rows={3}
                                        placeholder="OPTIONS may end services under this agreement by giving 3 calendar days notice..."
                                        hint="Leave blank for branch default (3-day or 10-day)" />

                                    <Divider label="ADMINISTERING MEDICATION" />
                                    <Field name="medication_text" label="Medication Administration" rows={3}
                                        placeholder="For those care recipients who require administration of medication..." />

                                    <Divider label="OUR CARE PROVIDERS CANNOT BE HIRED BY YOU" />
                                    <Field name="cannot_hire_text" label="Cannot Be Hired" rows={6}
                                        placeholder="You understand that OPTIONS is not a staffing agency..." />

                                    <Divider label="RECORD KEEPING" />
                                    <Field name="record_keeping_text" label="Record Keeping" rows={4}
                                        placeholder="It is standard policy and practice at OPTIONS..." />

                                    <Divider label="MILEAGE REIMBURSEMENT" />
                                    <Field name="mileage_reimbursement_text" label="Mileage Reimbursement" rows={3}
                                        placeholder="Mileage will be charged at the rate of $0.67 per mile..." />

                                    <Divider label="USE OF FAMILY VEHICLE" />
                                    <Field name="vehicle_use_text" label="Use of Family Vehicle" rows={2}
                                        placeholder='If you wish to authorize our care providers to drive...' />

                                    <Divider label="GENERAL PROVISIONS" />
                                    <Field name="general_provisions_text" label="General Provisions (governing state clause)" rows={2}
                                        placeholder="This Agreement shall be governed by the laws of..."
                                        hint="Leave blank to use the branch default governing state" />
                                </div>
                            )}

                            {/* ── PAGE 2 ── */}
                            {activeTab === 'page2' && (
                                <div>
                                    <SectionTitle>Page 2 — Patient Rights & Billing</SectionTitle>

                                    <Divider label="NOTICE OF PATIENTS' RIGHTS AND RESPONSIBILITIES" />
                                    <Field name="patients_rights_text" label="Patients' Rights Text" rows={12}
                                        placeholder="Enter patients' rights text..."
                                        hint="Leave blank to use the standard text for this branch's state" />

                                    <Divider label="NOTICE OF COMPLAINT PROCEDURES" />
                                    <Field name="complaint_procedures_text" label="Complaint Procedures Text" rows={10}
                                        placeholder="Enter complaint procedures text..."
                                        hint="Leave blank to use the standard text for this branch" />

                                    <Divider label="NOTICE OF BILLING PROCEDURES" />
                                    <Field name="billing_procedures_text" label="Billing Procedures Text" rows={10}
                                        placeholder="Enter billing procedures text..."
                                        hint="Leave blank to use the standard 5-item billing list" />

                                    <Divider label="EFT AUTHORIZATION (Page 3)" />
                                    <Field name="eft_authorization_text" label="EFT Authorization Text" rows={8}
                                        placeholder="Enter EFT authorization text..." />

                                    <Divider label="CONSUMER NOTICE (Page 3.1 — PA branches)" />
                                    <Field name="consumer_notice_text" label="Consumer Notice Text" rows={5}
                                        placeholder="Enter consumer notice text..." />
                                </div>
                            )}

                            {/* ── SETTINGS ── */}
                            {activeTab === 'settings' && (
                                <div>
                                    <SectionTitle>Branch Settings</SectionTitle>

                                    <div style={{ background: '#f8fafc', padding: '15px', borderRadius: '8px', marginBottom: '15px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                                            <input type="checkbox" name="has_initial_contact"
                                                checked={content.has_initial_contact || false} onChange={handleChange}
                                                style={{ width: '18px', height: '18px' }} />
                                            <span style={{ fontWeight: 'bold' }}>Requires Initial Contact Date</span>
                                        </label>
                                        <small style={{ color: '#64748b', marginLeft: '28px', display: 'block', marginTop: '4px' }}>
                                            Makes Initial Contact Date required in the agreement form (GA/SC branches)
                                        </small>
                                    </div>

                                    <div style={{ background: '#f8fafc', padding: '15px', borderRadius: '8px', marginBottom: '15px' }}>
                                        <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                                            <input type="checkbox" name="requires_consumer_notice"
                                                checked={content.requires_consumer_notice || false} onChange={handleChange}
                                                style={{ width: '18px', height: '18px' }} />
                                            <span style={{ fontWeight: 'bold' }}>Requires Consumer Notice Page (Page 3.1)</span>
                                        </label>
                                        <small style={{ color: '#64748b', marginLeft: '28px', display: 'block', marginTop: '4px' }}>
                                            Adds the Consumer Notice of Direct Care Worker Status page to the PDF (PA branches)
                                        </small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ fontWeight: '600', marginBottom: '6px', display: 'block' }}>Holiday Count</label>
                                        <select name="holiday_count" value={content.holiday_count || 11}
                                            onChange={handleChange} className="form-input">
                                            <option value="11">11 Holidays (Standard)</option>
                                            <option value="12">12 Holidays (Includes Easter Sunday)</option>
                                        </select>
                                        <small style={{ color: '#64748b' }}>Affects the Federal Holidays section</small>
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ fontWeight: '600', marginBottom: '6px', display: 'block' }}>Default Care Type</label>
                                        <input type="text" name="care_type" value={content.care_type || 'Home Care'}
                                            onChange={handleChange} className="form-input" />
                                    </div>

                                    <div className="form-group" style={{ marginBottom: '20px' }}>
                                        <label style={{ fontWeight: '600', marginBottom: '6px', display: 'block' }}>Special Instructions (internal notes)</label>
                                        <textarea name="special_instructions" value={content.special_instructions || ''}
                                            onChange={handleChange} rows={2} className="form-input"
                                            placeholder="Internal notes only — not shown in agreements" />
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>

                <div className="modal-footer" style={{
                    padding: '20px', borderTop: '1px solid #e2e8f0',
                    display: 'flex', gap: '10px', justifyContent: 'flex-end', background: '#f8fafc'
                }}>
                    {saveSuccess && (
                        <div style={{ color: '#10b981', fontSize: '14px', marginRight: 'auto' }}>✓ Saved successfully!</div>
                    )}
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                    <button className="action-btn" onClick={handleSave} disabled={saving}
                        style={{ background: saving ? '#94a3b8' : 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)', minWidth: '120px' }}>
                        {saving ? 'Saving...' : '💾 Save Template'}
                    </button>
                </div>
            </div>
        </div>
    );
};

const SectionTitle = ({ children }) => (
    <h4 style={{ marginBottom: '20px', color: '#0f172a', borderBottom: '1px solid #e2e8f0', paddingBottom: '8px' }}>
        {children}
    </h4>
);

const Divider = ({ label }) => (
    <div style={{ fontSize: '11px', fontWeight: '700', color: '#94a3b8', letterSpacing: '0.08em',
        textTransform: 'uppercase', marginBottom: '8px', marginTop: '4px',
        borderLeft: '3px solid #4facfe', paddingLeft: '8px' }}>
        {label}
    </div>
);

const TabButton = ({ active, onClick, children }) => (
    <button onClick={onClick} style={{
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
    onMouseOver={(e) => { if (!active) { e.currentTarget.style.background = '#f1f5f9'; e.currentTarget.style.color = '#0f172a'; } }}
    onMouseOut={(e) => { if (!active) { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#64748b'; } }}>
        {children}
    </button>
);

export default BranchContentEditor;
