import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../AuthContext'; 
import BranchDropdown from "./BranchDropdown";
import ShareModal from './ShareModal';
import BranchesList from './BranchesList';
import '../Dashboard.css'; 
import {endpoint} from '../resource/Constant';

const Dashboard = () => {
    const { token, logout } = useContext(AuthContext);
    const [activeTab, setActiveTab] = useState('new-agreement');
    const [agreements, setAgreements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isGenerating, setIsGenerating] = useState(false);
    const [freqError, setFreqError] = useState('');
    const [freqTouched, setFreqTouched] = useState(false);
    const [inicontactError, setInicontactError] = useState('');
    const [inicontactTouched, setInicontactTouched] = useState(false);
    const [inquiryDateError, setInquiryDateError] = useState('');
    const [inquiryDateTouched, setInquiryDateTouched] = useState(false);
    const [editingId, setEditingId] = useState(null);
    const [originalData, setOriginalData] = useState({});
    const [showShareModal, setShowShareModal] = useState(false);
    const [selectedAgreement, setSelectedAgreement] = useState(null);
    const [branches, setBranches] = useState([]);
    const [branchesLoading, setBranchesLoading] = useState(false);
    // Branch content stored for PDF generation only - NOT used to populate form fields
    const [branchContent, setBranchContent] = useState(null);

    const emptyForm = {
        clt_title: '', clt_first_name: '', clt_last_name: '', clt_address: '',
        clt_city: '', clt_state: '', clt_zip: '', clt_relationship: '',
        care_title: '', care_first_name: '', care_last_name: '',
        care_recipient_address: '', care_city: '', care_state: '', care_zip: '',
        branch_code: 'Select Branch', initial_inquiry_date: '',
        agreement_date: new Date().toISOString().split('T')[0],
        services_start_date: '', services_start_time: '', hourly_rate: '',
        inicontactdate: '', required_services: '', freq_of_visit: '',
        hazards: '', perc_charged: '100', handled_by: '', instructions_given_by: '',
    };

    const [formData, setFormData] = useState(emptyForm);

    // Fetch branch content for PDF generation and validation ONLY
    // Does NOT auto-populate any form fields
    const fetchBranchContent = async (branchCode) => {
        if (!branchCode || branchCode === 'Select Branch') return;
        try {
            const response = await fetch(`${endpoint}/branches/${branchCode}/content`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
            });
            if (response.ok) {
                const content = await response.json();
                setBranchContent(content);
                if (content.has_initial_contact) setInicontactTouched(true);
            }
        } catch (error) {
            console.error('Error fetching branch content:', error);
        }
    };

    const isGASCBranch = (branchCode) => {
        if (!branchCode) return false;
        const b = branchCode.toLowerCase();
        return ['scgahomecare','scgahomecare_staging','athomecare','athomecare_staging'].includes(b);
    };

    const validateInquiryDate = (v) => (!v || v.trim() === '') ? 'Initial Inquiry Date is required' : '';
    const validateInicontactDate = (branchCode, v) =>
        (isGASCBranch(branchCode) && (!v || v.trim() === '')) ? 'Initial Contact Date is required for GA/SC branches' : '';
    const validateFrequency = (value) => {
        if (!value || value.trim() === '') return '';
        const validPatterns = ['daily','weekly','bi-weekly','monthly','monday','tuesday','wednesday','thursday','friday','mon','tue','wed','thu','fri','every day','every weekday','weekends','once a week','twice a week','three times a week','every morning','every afternoon','every evening','24/7','24 hours','around the clock'];
        const lower = value.toLowerCase().trim();
        const isValid = validPatterns.some(p => lower.includes(p)) ||
            /\d+\s*(?:times?|x)\s*(?:per|a|each)\s*(?:day|week|month)/i.test(value) ||
            /every\s+\d+\s*(?:hours?|days?)/i.test(value) ||
            /(?:mon|tue|wed|thu|fri|sat|sun)(?:day)?\s*(?:-|\s+to\s+)?/i.test(value);
        return isValid ? '' : 'Please enter a valid frequency (e.g., Daily, Weekly, Mon-Fri, 3 times per week)';
    };

    const getBranchDisplayName = (branchCode) => {
        if (!branchCode || !branches.length) return branchCode;
        const branch = branches.find(b => b.branch_code === branchCode);
        return branch ? branch.branch_name : branchCode;
    };

    useEffect(() => {
        setFormData(prev => ({ ...prev, responsible_party: `${prev.clt_first_name} ${prev.clt_last_name}`.trim() }));
    }, [formData.clt_first_name, formData.clt_last_name]);

    const fetchBranches = async () => {
        setBranchesLoading(true);
        try {
            const response = await fetch(`${endpoint}/branches?t=${new Date().getTime()}`, {
                method: 'GET', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
                mode: 'cors', credentials: 'include',
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            setBranches(await response.json());
        } catch (err) { console.error("Error fetching branches:", err); }
        finally { setBranchesLoading(false); }
    };

    const fetchData = async () => {
        if (!token) return;
        setLoading(true);
        try {
            const response = await fetch(`${endpoint}/agreements`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json', 'Accept': 'application/json' },
                mode: 'cors', credentials: 'include',
            });
            if (response.status === 401) { logout(); return; }
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            setAgreements(Array.isArray(data) ? data.sort((a, b) => b.id - a.id) : []);
        } catch (err) { console.error("Fetch error:", err); }
        finally { setLoading(false); }
    };

    useEffect(() => { fetchData(); fetchBranches(); }, [token]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({ ...prev, [name]: type === 'checkbox' ? checked : value }));
        if (name === 'freq_of_visit') setFreqError(validateFrequency(value));
        if (name === 'inicontactdate') setInicontactError(validateInicontactDate(formData.branch_code, value));
        if (name === 'initial_inquiry_date') setInquiryDateError(validateInquiryDate(value));
    };

    const handleFreqBlur = () => { setFreqTouched(true); setFreqError(validateFrequency(formData.freq_of_visit)); };
    const handleInicontactBlur = () => { setInicontactTouched(true); setInicontactError(validateInicontactDate(formData.branch_code, formData.inicontactdate)); };
    const handleInquiryDateBlur = () => { setInquiryDateTouched(true); setInquiryDateError(validateInquiryDate(formData.initial_inquiry_date)); };

    const handleBranchSelect = (branchData) => {
        if (!branchData || !branchData.branch_code) return;
        setFormData(prev => ({ ...prev, branch_code: branchData.branch_code }));
        // Fetch for PDF/validation only - NO form field population
        fetchBranchContent(branchData.branch_code);
        setInicontactError(validateInicontactDate(branchData.branch_code, formData.inicontactdate));
        if (isGASCBranch(branchData.branch_code) && !formData.inicontactdate) setInicontactTouched(true);
    };

    const handleEdit = async (agreementId) => {
        try {
            const response = await fetch(`${endpoint}/agreements/${agreementId}`, {
                method: 'GET',
                headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json', 'Accept': 'application/json' },
                mode: 'cors', credentials: 'include',
            });
            if (!response.ok) throw new Error('Failed to fetch agreement');
            const agreement = await response.json();
            setFormData({
                clt_title: agreement.clt_title || '', clt_first_name: agreement.clt_first_name || '',
                clt_last_name: agreement.clt_last_name || '', clt_address: agreement.clt_address || '',
                clt_city: agreement.clt_city || '', clt_state: agreement.clt_state || '',
                clt_zip: agreement.clt_zip || '', clt_relationship: agreement.clt_relationship || 'Self',
                care_title: agreement.care_title || '', care_first_name: agreement.care_first_name || '',
                care_last_name: agreement.care_last_name || '', care_recipient_address: agreement.care_recipient_address || '',
                care_city: agreement.care_city || '', care_state: agreement.care_state || '',
                care_zip: agreement.care_zip || '', branch_code: agreement.branch_code || 'Select Branch',
                initial_inquiry_date: agreement.initial_inquiry_date || '',
                agreement_date: agreement.agreement_date || new Date().toISOString().split('T')[0],
                services_start_date: agreement.start_date || '', services_start_time: agreement.services_start_time || '',
                hourly_rate: agreement.hourly_rate || '', inicontactdate: agreement.inicontactdate || '',
                required_services: agreement.required_services || '', freq_of_visit: agreement.freq_of_visit || '',
                hazards: agreement.hazards || '', perc_charged: agreement.perc_charged || '100',
                handled_by: agreement.handled_by || '', instructions_given_by: agreement.instructions_given_by || '',
            });
            setFreqError(''); setFreqTouched(false); setInicontactError(''); setInicontactTouched(false);
            setInquiryDateError(''); setInquiryDateTouched(false);
            setOriginalData(agreement); setEditingId(agreementId); setActiveTab('new-agreement');
        } catch (error) { console.error('Error fetching agreement:', error); alert('Failed to load agreement for editing'); }
    };

    const viewPDF = async (id, recipientLast) => {
        try {
            const response = await fetch(`${endpoint}/agreements/${id}/pdf`, {
                method: 'GET', headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/pdf' },
                mode: 'cors', credentials: 'include',
            });
            if (!response.ok) throw new Error('Failed to load PDF');
            const url = window.URL.createObjectURL(await response.blob());
            window.open(url, '_blank');
            setTimeout(() => window.URL.revokeObjectURL(url), 1000);
        } catch (err) { alert("Failed to load PDF. Please try again."); }
    };

    const handleShare = (agreement) => { setSelectedAgreement(agreement); setShowShareModal(true); };

    const clearValidations = () => {
        setFreqError(''); setFreqTouched(false); setInicontactError('');
        setInicontactTouched(false); setInquiryDateError(''); setInquiryDateTouched(false);
    };

    const handleSubmitAgreement = async (e) => {
        e.preventDefault();
        const iqErr = validateInquiryDate(formData.initial_inquiry_date);
        if (iqErr) { setInquiryDateError(iqErr); setInquiryDateTouched(true); alert('Please enter Initial Inquiry Date'); return; }
        const fqErr = validateFrequency(formData.freq_of_visit);
        if (fqErr) { setFreqError(fqErr); setFreqTouched(true); alert('Please fix the frequency format before submitting.'); return; }
        const icErr = validateInicontactDate(formData.branch_code, formData.inicontactdate);
        if (icErr) { setInicontactError(icErr); setInicontactTouched(true); alert(icErr); return; }

        setIsGenerating(true);
        const cleanedData = {};
        for (const [key, value] of Object.entries(formData)) {
            if (value !== null && value !== undefined && value !== '' && value !== 'Select Branch') cleanedData[key] = value;
        }
        const submissionData = {
            ...cleanedData,
            hourly_rate: parseFloat(formData.hourly_rate) || 0.0,
            mileage_rate: 0.0,
            start_date: formData.services_start_date || null,
            services_start_time: formData.services_start_time || null,
            inicontactdate: formData.inicontactdate || null,
            required_services: formData.required_services || '',
            freq_of_visit: formData.freq_of_visit || '',
            hazards: formData.hazards || '',
            perc_charged: formData.perc_charged || '100',
            rep_signature: formData.rep_signature || "Staff Signed",
            care_dob: formData.care_dob || null,
            end_date: null, date_of_order: null,
            care_type: branchContent?.care_type || 'Home Care',
        };

        try {
            let response;
            if (editingId) {
                const changedData = {};
                for (const [key, value] of Object.entries(submissionData)) {
                    if (JSON.stringify(value) !== JSON.stringify(originalData[key])) changedData[key] = value;
                }
                if (Object.keys(changedData).length === 0) { alert('No changes detected'); setIsGenerating(false); return; }
                response = await fetch(`${endpoint}/agreements/${editingId}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`, 'Accept': 'application/json' },
                    mode: 'cors', credentials: 'include', body: JSON.stringify(changedData)
                });
            } else {
                response = await fetch(`${endpoint}/agreements`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}`, 'Accept': 'application/json' },
                    mode: 'cors', credentials: 'include', body: JSON.stringify(submissionData)
                });
            }
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                const errorFields = Array.isArray(errorData.detail)
                    ? errorData.detail.map(err => `${err.loc[1]}: ${err.msg}`).join("\n")
                    : errorData.detail || "Unknown error";
                alert("Validation Error:\n" + errorFields);
                return;
            }
            alert(editingId ? "Agreement updated successfully!" : "Agreement successfully saved!");
            setEditingId(null); setOriginalData({}); setBranchContent(null);
            setFormData({ ...emptyForm, agreement_date: new Date().toISOString().split('T')[0] });
            clearValidations();
            await fetchData();
        } catch (err) { alert(`Server connection failed: ${err.message}`); }
        finally { setIsGenerating(false); }
    };

    const handleReset = () => {
        if (editingId) {
            if (window.confirm('Discard changes and reset form?')) { setEditingId(null); setOriginalData({}); setBranchContent(null); }
            else return;
        }
        setFormData({ ...emptyForm, agreement_date: new Date().toISOString().split('T')[0] });
        clearValidations();
    };

    const downloadPDF = async (id, recipientLast) => {
        try {
            const response = await fetch(`${endpoint}/agreements/${id}/pdf`, {
                method: 'GET', headers: { 'Authorization': `Bearer ${token}`, 'Accept': 'application/pdf' },
                mode: 'cors', credentials: 'include',
            });
            if (!response.ok) throw new Error('Failed to download PDF');
            const url = window.URL.createObjectURL(await response.blob());
            const link = document.createElement('a');
            link.href = url; link.setAttribute('download', `Agreement_${recipientLast}.pdf`);
            document.body.appendChild(link); link.click(); link.remove();
            window.URL.revokeObjectURL(url);
        } catch (err) { alert("Failed to download PDF. Please try again."); }
    };

    if (loading) return <div className="loading-center">Loading Management Portal...</div>;

    return (
        <div className="page-wrapper">
            <nav className="sidebar">
                <div className="logo">CARE<span>PORTAL</span></div>
                <div className="nav-group">
                    <div className={`nav-item ${activeTab === 'new-agreement' ? 'active' : ''}`}
                        onClick={() => { setActiveTab('new-agreement'); handleReset(); }}>
                        Create Agreement
                    </div>
                    <div className={`nav-item ${activeTab === 'documents' ? 'active' : ''}`}
                        onClick={() => setActiveTab('documents')}>
                        Official Agreements
                    </div>
                    <div className={`nav-item ${activeTab === 'branches' ? 'active' : ''}`}
                        onClick={() => setActiveTab('branches')}>
                        Manage Branches
                    </div>
                </div>
                <div className="sidebar-footer">
                    <button onClick={logout} className="logout-btn">Sign Out</button>
                </div>
            </nav>

            <main className="main-content">
                <header className="header-area">
                    <h1 className="greeting">
                        {activeTab === 'new-agreement' && 'Create New Agreement'}
                        {activeTab === 'documents' && 'Official Agreements'}
                        {activeTab === 'branches' && 'Branch Management'}
                    </h1>
                </header>

                {activeTab === 'new-agreement' && (
                    <div className="glass-card animate-fade-in form-container-wide">
                        <form onSubmit={handleSubmitAgreement}>
                            <div className="form-header-row">
                                <h2 className="form-title">{editingId ? 'Edit Agreement' : 'Service Agreement Intake'}</h2>
                                <div className="invoice-date">Date: {formData.agreement_date}</div>
                            </div>

                            <div className="section-divider"><span className="section-label">1. Responsible Party (Payer)</span></div>
                            <div className="form-grid-3">
                                <div className="form-group">
                                    <label>First Name</label>
                                    <input name="clt_first_name" className="form-input" value={formData.clt_first_name} onChange={handleChange} required />
                                </div>
                                <div className="form-group">
                                    <label>Last Name</label>
                                    <input name="clt_last_name" className="form-input" value={formData.clt_last_name} onChange={handleChange} required />
                                </div>
                                <div className="form-group">
                                    <label>Relationship</label>
                                    <select name="clt_relationship" className="form-input" value={formData.clt_relationship} onChange={handleChange}>
                                        <option value="Self">Self</option>
                                        <option value="Daughter">Daughter</option>
                                        <option value="Son">Son</option>
                                        <option value="Spouse">Spouse</option>
                                        <option value="Other">Other</option>
                                    </select>
                                </div>
                                <div className="form-group span-2">
                                    <label>Street Address</label>
                                    <input name="clt_address" className="form-input" value={formData.clt_address} onChange={handleChange} required />
                                </div>
                                <div className="form-group">
                                    <label>City</label>
                                    <input name="clt_city" className="form-input" value={formData.clt_city} onChange={handleChange} required />
                                </div>
                            </div>

                            <div className="section-divider"><span className="section-label">2. Care Recipient</span></div>
                            <div className="form-grid-3">
                                <div className="form-group">
                                    <label>First Name</label>
                                    <input name="care_first_name" className="form-input" value={formData.care_first_name} onChange={handleChange} required />
                                </div>
                                <div className="form-group">
                                    <label>Last Name</label>
                                    <input name="care_last_name" className="form-input" value={formData.care_last_name} onChange={handleChange} required />
                                </div>
                                <div className="form-group">
                                    <label>Care Address</label>
                                    <input name="care_recipient_address" className="form-input" value={formData.care_recipient_address} onChange={handleChange} />
                                </div>
                            </div>

                            <div className="section-divider"><span className="section-label">3. Office Administration &amp; Schedule</span></div>
                            <div className="admin-row-grid">
                                <div className="form-group">
                                    <label>Initial Inquiry Date <span style={{color: 'red'}}>*</span></label>
                                    <input type="date" name="initial_inquiry_date"
                                        className={`form-input ${inquiryDateTouched && inquiryDateError ? 'input-error' : ''}`}
                                        value={formData.initial_inquiry_date} onChange={handleChange} onBlur={handleInquiryDateBlur} required />
                                    {inquiryDateTouched && inquiryDateError && (
                                        <div className="error-message" style={{color:'#ef4444',fontSize:'12px',marginTop:'5px'}}>{inquiryDateError}</div>
                                    )}
                                </div>
                                <div className="form-group">
                                    <label>
                                        Initial Contact Date (GA/SC &amp; Atlanta Home Care)
                                        {isGASCBranch(formData.branch_code) && <span style={{color:'red',marginLeft:'5px'}}>*</span>}
                                    </label>
                                    <input type="date" name="inicontactdate"
                                        className={`form-input ${inicontactTouched && inicontactError ? 'input-error' : ''}`}
                                        value={formData.inicontactdate} onChange={handleChange} onBlur={handleInicontactBlur}
                                        required={isGASCBranch(formData.branch_code)} />
                                    {inicontactTouched && inicontactError && (
                                        <div className="error-message" style={{color:'#ef4444',fontSize:'12px',marginTop:'5px'}}>{inicontactError}</div>
                                    )}
                                </div>
                                <div className="form-group"></div>
                            </div>

                            <div className="admin-row-grid">
                                <div className="form-group">
                                    <label>Instructions Given By</label>
                                    <input name="instructions_given_by" className="form-input" value={formData.instructions_given_by} onChange={handleChange} placeholder="Full Name" />
                                </div>
                                <div className="form-group">
                                    <label>Services Start Date</label>
                                    <input type="date" name="services_start_date" className="form-input" value={formData.services_start_date} onChange={handleChange} />
                                </div>
                                <div className="form-group">
                                    <label>Services Start Time</label>
                                    <input name="services_start_time" className="form-input" value={formData.services_start_time} onChange={handleChange} placeholder="e.g. 9:00 AM" />
                                </div>
                            </div>

                            <div className="admin-row-grid">
                                <div className="form-group">
                                    <label>Handled By (Staff)</label>
                                    <input name="handled_by" className="form-input" value={formData.handled_by} onChange={handleChange} required />
                                </div>
                                <div className="form-group"></div>
                                <div className="form-group"></div>
                            </div>

                            <div className="section-divider"><span className="section-label">4. Service Details</span></div>
                            <div className="admin-row-grid">
                                <div className="form-group">
                                    <BranchDropdown onBranchChange={handleBranchSelect} selectedValue={formData.branch_code} />
                                </div>
                                <div className="form-group">
                                    <label>Hourly Rate ($)</label>
                                    <input name="hourly_rate" type="number" step="0.01" className="form-input" value={formData.hourly_rate} onChange={handleChange} />
                                </div>
                                <div className="form-group">
                                    <label>Percentage Charged (%)</label>
                                    <input name="perc_charged" type="number" className="form-input" value={formData.perc_charged} onChange={handleChange} min="0" max="100" />
                                </div>
                            </div>

                            <div className="admin-row-grid">
                                <div className="form-group span-2">
                                    <label>Required Services</label>
                                    <textarea name="required_services" className="form-input" value={formData.required_services} onChange={handleChange} rows="3" />
                                </div>
                                <div className="form-group">
                                    <label>Frequency of Visits</label>
                                    <input name="freq_of_visit"
                                        className={`form-input ${freqTouched && freqError ? 'input-error' : ''}`}
                                        value={formData.freq_of_visit} onChange={handleChange} onBlur={handleFreqBlur}
                                        placeholder="e.g. Daily, Weekly, Mon-Fri, 3 times per week" />
                                    {freqTouched && freqError && (
                                        <div className="error-message" style={{color:'#ef4444',fontSize:'12px',marginTop:'5px'}}>{freqError}</div>
                                    )}
                                </div>
                            </div>

                            <div className="admin-row-grid">
                                <div className="form-group span-2">
                                    <label>Hazards</label>
                                    <textarea name="hazards" className="form-input" value={formData.hazards} onChange={handleChange} rows="2" placeholder="None Reported" />
                                </div>
                            </div>

                            <div className="form-actions-row">
                                <button type="submit" className="action-btn submit-flex" disabled={isGenerating}>
                                    {isGenerating ? "Processing..." : (editingId ? "Update Agreement" : "Submit Agreement")}
                                </button>
                                <button type="button" onClick={handleReset} className="cancel-btn">
                                    {editingId ? 'Cancel Edit' : 'Reset Form'}
                                </button>
                            </div>
                        </form>
                    </div>
                )}

                {activeTab === 'documents' && (
                    <div className="glass-card animate-fade-in" style={{padding:'0',overflow:'hidden'}}>
                        {branchesLoading ? <div className="loading-center">Loading branches...</div> : (
                            <table className="data-table">
                                <thead>
                                    <tr>
                                        <th className="p-20">Client Name</th>
                                        <th className="p-20">Branch</th>
                                        <th className="p-20">Rate</th>
                                        <th className="p-20">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {agreements.length > 0 ? agreements.map(ag => (
                                        <tr key={ag.id}>
                                            <td className="p-20"><strong>{ag.clt_first_name} {ag.clt_last_name}</strong></td>
                                            <td className="p-20">{getBranchDisplayName(ag.branch_code)}</td>
                                            <td className="p-20">${ag.hourly_rate}/hr</td>
                                            <td className="p-20 actions-cell">
                                                <button onClick={() => handleEdit(ag.id)} className="action-btn small edit-btn">Edit</button>
                                                <button onClick={() => viewPDF(ag.id, ag.clt_last_name)} className="action-btn small view-btn">View</button>
                                                <button onClick={() => handleShare(ag)} className="action-btn small share-btn">Share</button>
                                                <button onClick={() => downloadPDF(ag.id, ag.clt_last_name)} className="action-btn small download-btn">Download</button>
                                            </td>
                                        </tr>
                                    )) : (
                                        <tr><td colSpan="4" className="p-20 text-center">No agreements found.</td></tr>
                                    )}
                                </tbody>
                            </table>
                        )}
                    </div>
                )}

                {activeTab === 'branches' && (
                    <div className="glass-card animate-fade-in">
                        <BranchesList token={token} />
                    </div>
                )}

                <ShareModal
                    isOpen={showShareModal}
                    onClose={() => { setShowShareModal(false); setSelectedAgreement(null); }}
                    agreementId={selectedAgreement?.id}
                    agreementName={selectedAgreement ? `${selectedAgreement.clt_first_name || ''} ${selectedAgreement.clt_last_name || ''}`.trim() : ''}
                    token={token}
                />
            </main>
        </div>
    );
};

export default Dashboard;
