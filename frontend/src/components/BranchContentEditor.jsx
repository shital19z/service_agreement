
import React, { useState, useEffect, useCallback } from 'react';
import { endpoint } from '../resource/Constant';


const Field = ({ label, name, rows, placeholder, hint, content, onChange }) => (
    <div className="form-group" style={{ marginBottom: '20px' }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontWeight: '600', marginBottom: '6px' }}>
            <span style={{ color: '#4facfe', fontSize: '14px' }}>✨</span> {label}
        </label>
        {rows ? (
            <textarea name={name} value={content[name] || ''} onChange={onChange}
                rows={rows} className="form-input" placeholder={placeholder || ''} />
        ) : (
            <input type="text" name={name} value={content[name] || ''} onChange={onChange}
                className="form-input" placeholder={placeholder || ''} />
        )}
        {hint && <small style={{ color: '#64748b', display: 'block', marginTop: '4px' }}>{hint}</small>}
    </div>
);

const NumberField = ({ label, name, step, min, max, defaultVal, hint, content, onChange }) => (
    <div className="form-group" style={{ marginBottom: '20px' }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '5px', fontWeight: '600', marginBottom: '6px' }}>
            <span style={{ color: '#4facfe', fontSize: '14px' }}>✨</span> {label}
        </label>
        <input type="number" name={name} value={content[name] ?? defaultVal}
            onChange={onChange} step={step || '1'} min={min} max={max} className="form-input" />
        {hint && <small style={{ color: '#64748b', display: 'block', marginTop: '4px' }}>{hint}</small>}
    </div>
);
// ─────────────────────────────────────────────────────────────────────────────

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

    // useCallback prevents handleChange from being recreated on every render
    const handleChange = useCallback((e) => {
        const { name, value, type, checked } = e.target;
        setContent(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    }, []);

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

    const tabs = [
        { key: 'page1',    label: 'Page 1',               icon: '✨' },
        { key: 'page1cont',label: 'Page 1 Cont',          icon: '✨' },
        { key: 'page2',    label: 'Page 2',               icon: '✨' },
        { key: 'page3',    label: 'Page 3 (EFT)',         icon: '✨' },
        { key: 'page3_1',  label: 'Page 3.1 (Consumer)',  icon: '✨' },
        { key: 'settings', label: 'Settings',             icon: null },
    ];

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
                    <div style={{ display: 'flex', borderBottom: '2px solid #e2e8f0', marginBottom: '20px', flexWrap: 'wrap', gap: '2px' }}>
                        {tabs.map(tab => (
                            <TabButton key={tab.key} active={activeTab === tab.key} onClick={() => setActiveTab(tab.key)}>
                                {tab.label}
                                {tab.icon && <span style={{ fontSize: '10px', marginLeft: '4px', color: '#4facfe' }}>{tab.icon}</span>}
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
                                    <PageBanner>📄 <strong>These fields control PDF Page 1.</strong> Leave any field blank to use the default text.</PageBanner>

                                    <Divider label="CHARGES / BILLING INTRO" />
                                    <Field name="charges_text" label="Charges Section Text" rows={3}
                                        placeholder="We bill bi-weekly for services rendered..."
                                        hint="Introductory text for the CHARGES section on Page 1"
                                        content={content} onChange={handleChange} />

                                    <Divider label="PAYMENT OBLIGATIONS" />
                                    <Field name="payment_obligations_text" label="Payment Obligations Text" rows={4}
                                        placeholder="The parties responsible for payment include..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="FEDERAL HOLIDAYS" />
                                    <Field name="federal_holidays_text" label="Federal Holidays Text" rows={3}
                                        placeholder="When services are required on Federal holidays..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="LIVE-IN SERVICES" />
                                    <Field name="live_in_text" label="Live-In Services & Care Provider Schedule" rows={5}
                                        placeholder="OPTIONS care providers who provide live-in services..."
                                        content={content} onChange={handleChange} />
                                </div>
                            )}

                            {/* ── PAGE 1 CONT ── */}
                            {activeTab === 'page1cont' && (
                                <div>
                                    <SectionTitle>Page 1 Continuation — Additional Terms</SectionTitle>
                                    <PageBanner>📄 <strong>These fields control PDF Page 1 Continuation (Page 2 of the PDF).</strong> Leave any field blank to use the default text.</PageBanner>

                                    <Divider label="MILEAGE RATE" />
                                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 3fr', gap: '15px', marginBottom: '20px' }}>
                                        <NumberField name="mileage_rate" label="Mileage Rate ($/mile)" step="0.01" defaultVal={0.67}
                                            hint="Branch-level default mileage rate"
                                            content={content} onChange={handleChange} />
                                    </div>

                                    <Divider label="NEEDS ASSESSMENT & PLAN OF CARE" />
                                    <Field name="needs_assessment_text" label="Needs Assessment & Plan of Care" rows={3}
                                        placeholder="When a Needs Assessment and a Plan of Care is conducted..."
                                        hint="Leave blank to use branch default"
                                        content={content} onChange={handleChange} />

                                    <Divider label="YOUR VALUABLES" />
                                    <Field name="valuables_text" label="Your Valuables" rows={3}
                                        placeholder="Our care providers are not authorized to accept payments..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="NOTICE PERIOD" />
                                    <Field name="notice_period_text" label="Notice Period" rows={3}
                                        placeholder="OPTIONS may end services under this agreement by giving 3 calendar days notice..."
                                        hint="Leave blank for branch default (3-day or 10-day)"
                                        content={content} onChange={handleChange} />

                                    <Divider label="ADMINISTERING MEDICATION" />
                                    <Field name="medication_text" label="Medication Administration" rows={3}
                                        placeholder="For those care recipients who require administration of medication..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="OUR CARE PROVIDERS CANNOT BE HIRED BY YOU" />
                                    <Field name="cannot_hire_text" label="Cannot Be Hired" rows={6}
                                        placeholder="You understand that OPTIONS is not a staffing agency..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="RECORD KEEPING" />
                                    <Field name="record_keeping_text" label="Record Keeping" rows={4}
                                        placeholder="It is standard policy and practice at OPTIONS..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="MILEAGE REIMBURSEMENT" />
                                    <Field name="mileage_reimbursement_text" label="Mileage Reimbursement" rows={3}
                                        placeholder="Mileage will be charged at the rate of $0.67 per mile..."
                                        content={content} onChange={handleChange} />

                                    <Divider label="USE OF FAMILY VEHICLE" />
                                    <Field name="vehicle_use_text" label="Use of Family Vehicle" rows={2}
                                        placeholder='If you wish to authorize our care providers to drive...'
                                        content={content} onChange={handleChange} />

                                    <Divider label="GENERAL PROVISIONS" />
                                    <Field name="general_provisions_text" label="General Provisions (governing state clause)" rows={2}
                                        placeholder="This Agreement shall be governed by the laws of..."
                                        hint="Leave blank to use the branch default governing state"
                                        content={content} onChange={handleChange} />
                                </div>
                            )}

                            {/* ── PAGE 2 ── */}
                            {activeTab === 'page2' && (
                                <div>
                                    <SectionTitle>Page 2 — Patient Rights & Billing</SectionTitle>
                                    <PageBanner>📄 <strong>These fields control PDF Page 3 (Patient Rights & Billing Procedures).</strong> Leave any field blank to use the default text for this branch's state.</PageBanner>

                                    <Divider label="NOTICE OF PATIENTS' RIGHTS AND RESPONSIBILITIES" />
                                    <Field name="patients_rights_text" label="Patients' Rights Text" rows={12}
                                        placeholder="Enter patients' rights text..."
                                        hint="Leave blank to use the standard text for this branch's state"
                                        content={content} onChange={handleChange} />

                                    <Divider label="NOTICE OF COMPLAINT PROCEDURES" />
                                    <Field name="complaint_procedures_text" label="Complaint Procedures Text" rows={10}
                                        placeholder="Enter complaint procedures text..."
                                        hint="Leave blank to use the standard text for this branch"
                                        content={content} onChange={handleChange} />

                                    <Divider label="NOTICE OF BILLING PROCEDURES" />
                                    <Field name="billing_procedures_text" label="Billing Procedures Text" rows={10}
                                        placeholder="Enter billing procedures text..."
                                        hint="Leave blank to use the standard 5-item billing list"
                                        content={content} onChange={handleChange} />
                                </div>
                            )}

                            {/* ── PAGE 3 (EFT) ── */}
                            {activeTab === 'page3' && (
                                <div>
                                    <SectionTitle>Page 3 — EFT Authorization</SectionTitle>
                                    <PageBanner>📄 <strong>These fields control PDF Page 4 (Electronic Funds Transfer Authorization).</strong> Leave blank to use the default EFT text.</PageBanner>

                                    <Divider label="EFT AUTHORIZATION TEXT" />
                                    <Field name="eft_authorization_text" label="EFT Authorization Text" rows={10}
                                        placeholder="I, the undersigned, acknowledge that invoices prepared by Options for Senior America (Options) are due upon receipt..."
                                        hint="Leave blank to use the standard EFT authorization text"
                                        content={content} onChange={handleChange} />
                                </div>
                            )}

                            {/* ── PAGE 3.1 (Consumer Notice) ── */}
                            {activeTab === 'page3_1' && (
                                <div>
                                    <SectionTitle>Page 3.1 — Consumer Notice of Direct Care Worker Status</SectionTitle>
                                    <PageBanner>📄 <strong>This page appears only for specific branches (PA — hbhomecare, nspahomecare).</strong> Enable it in Settings → "Requires Consumer Notice Page".</PageBanner>

                                    <div style={{ background: '#f0fdf4', border: '1px solid #86efac', borderRadius: '6px', padding: '10px 14px', marginBottom: '16px', fontSize: '12px', color: '#166534' }}>
                                        ℹ️ The Consumer Notice page is controlled by the <strong>"Requires Consumer Notice Page"</strong> toggle in the <strong>Settings</strong> tab.
                                        This tab lets you customize the insurance text shown on that page.
                                    </div>

                                    <Divider label="CONSUMER NOTICE INSURANCE TEXT" />
                                    <Field name="consumer_notice_text" label="Consumer Notice Text" rows={6}
                                        placeholder="I have been informed that Options For Senior America maintains general, professional liability, and workers compensation insurance covering the direct care worker who is employed by Options as an independent contractor."
                                        hint="Leave blank to use the default insurance notice text"
                                        content={content} onChange={handleChange} />
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

const PageBanner = ({ children }) => (
    <div style={{ background: '#fff3cd', border: '1px solid #ffc107', borderRadius: '6px', padding: '8px 12px', marginBottom: '16px', fontSize: '12px', color: '#856404' }}>
        {children}
    </div>
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
        padding: '10px 16px',
        background: active ? '#4facfe' : 'transparent',
        color: active ? 'white' : '#64748b',
        border: 'none',
        borderBottom: active ? '3px solid #2563eb' : 'none',
        cursor: 'pointer',
        fontWeight: active ? '600' : '400',
        fontSize: '13px',
        transition: 'all 0.2s'
    }}
    onMouseOver={(e) => { if (!active) { e.currentTarget.style.background = '#f1f5f9'; e.currentTarget.style.color = '#0f172a'; } }}
    onMouseOut={(e) => { if (!active) { e.currentTarget.style.background = 'transparent'; e.currentTarget.style.color = '#64748b'; } }}>
        {children}
    </button>
);

export default BranchContentEditor;