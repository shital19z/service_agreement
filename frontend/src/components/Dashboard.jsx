import React, { useState, useEffect, useContext, useRef } from 'react';
import { AuthContext } from '../AuthContext'; 
import BranchDropdown from "./BranchDropdown";
import SignatureCanvas from 'react-signature-canvas';
import '../Dashboard.css'; 

const Dashboard = () => {
    const { token, logout } = useContext(AuthContext);
    const sigCanvas = useRef({}); 
    
    const [activeTab, setActiveTab] = useState('dashboard');
    const [agreements, setAgreements] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isGenerating, setIsGenerating] = useState(false);
    const [showForm, setShowForm] = useState(false);
    const [serverOnline, setServerOnline] = useState(true);
    
    const [formData, setFormData] = useState({
    clt_title: 'Mr.',
    clt_first_name: '',
    clt_last_name: '',
    clt_address: '',
    clt_city: '',
    clt_state: 'MD',
    clt_zip: '',
    clt_relationship: '',

    care_title: 'Mrs.',
    care_first_name: '', 
    care_last_name: '',  
    care_recipient_address: '',
    care_city: '',
    care_state: '',
    care_zip: '',

    branch_code: 'Select Branch',
    initial_inquiry_date: '',
    agreement_date: new Date().toISOString().split('T')[0],
    start_date: '',
    services_start_time: '',
    care_type: '',
    hourly_rate: '',
});

    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            responsible_party: `${prev.clt_first_name} ${prev.clt_last_name}`.trim()
        }));
    }, [formData.clt_first_name, formData.clt_last_name]);

    const checkServerHealth = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/health');
            setServerOnline(response.ok);
        } catch (err) { setServerOnline(false); }
    };

    const fetchData = async () => {
        if (!token) return;
        try {
            const response = await fetch('http://127.0.0.1:8000/agreements', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.status === 401) { logout(); return; }
            const data = await response.json();
            if (response.ok) setAgreements(Array.isArray(data) ? data : []);
        } catch (err) { console.error("Fetch error:", err); } 
        finally { setLoading(false); }
    };

    useEffect(() => { 
        fetchData();
        checkServerHealth();
    }, [token]);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({ 
            ...prev, 
            [name]: type === 'checkbox' ? checked : value 
        }));
    };

const handleBranchSelect = (branchData) => {
    if (!branchData || !branchData.branch_code) {
        console.warn("Branch selection received empty data.");
        return;
    }
    
    console.log("Selected Branch Data:", branchData);
    
    setFormData(prev => ({ 
        ...prev, 
        branch_code: branchData.branch_code
    }));
};
    const clearSignature = () => sigCanvas.current.clear();

    const handleCreateAgreement = async (e) => {
        e.preventDefault();
        if (sigCanvas.current.isEmpty()) return alert("Signature required");
        setIsGenerating(true);

        const signatureImage = sigCanvas.current.getCanvas().toDataURL('image/png');

        
        const submissionData = {
            ...formData,
            hourly_rate: parseFloat(formData.hourly_rate) || 0.0,
            mileage_rate: parseFloat(formData.mileage_rate) || 0.0,
            client_signature: signatureImage,
            rep_signature: formData.rep_signature || "Staff Signed",
            care_dob: formData.care_dob || null,
            start_date: formData.start_date || new Date().toISOString().split('T')[0],
            end_date: formData.end_date || null,
        };
        console.log("FINAL DATA SENDING TO PYTHON:", submissionData);

        try {
            const response = await fetch('http://127.0.0.1:8000/agreements', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json', 
                    'Authorization': `Bearer ${token}` 
                },
                body: JSON.stringify(submissionData)
            });

            const result = await response.json();

            if (!response.ok) {
                console.error("VALIDATION FAILED:", result.detail);
                const errorFields = result.detail.map(err => `${err.loc[1]}: ${err.msg}`).join("\n");
                alert("Validation Error:\n" + errorFields);
                return;
            }

            alert("Agreement successfully saved!");
            setShowForm(false);
            fetchData(); 
        } catch (err) { 
            console.error("Server Error:", err);
            alert("Server connection failed."); 
        } finally { 
            setIsGenerating(false); 
        }
    };

    const downloadPDF = async (id, recipientLast) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/agreements/${id}/pdf`, {
                headers: { 'Authorization': `Bearer ${token}` },
            });
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `Agreement_${recipientLast}.pdf`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (err) { console.error("PDF Download Error:", err); }
    };

    if (loading) return <div className="loading-center">Loading Management Portal...</div>;

    return (
        <div className="page-wrapper">
            <nav className="sidebar">
                <div className="logo">CARE<span>PORTAL</span></div>
                <div className="nav-group">
                    <div className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => {setActiveTab('dashboard'); setShowForm(false);}}>Dashboard</div>
                    <div className={`nav-item ${activeTab === 'documents' ? 'active' : ''}`} onClick={() => {setActiveTab('documents'); setShowForm(false);}}>Document Vault</div>
                </div>
                <div className="sidebar-footer">
                    <button onClick={logout} className="logout-btn">Sign Out</button>
                </div>
            </nav>

            <main className="main-content">
                <header className="header-area">
                    <h1 className="greeting">Management Console</h1>
                    <div className="status-badge">
                        <div className="pulse-dot" style={{ backgroundColor: serverOnline ? '#10b981' : '#ef4444' }}></div>
                        {serverOnline ? 'System Online' : 'Server Offline'}
                    </div>
                </header>

                {activeTab === 'dashboard' && (
                    showForm ? (
                        <div className="glass-card animate-fade-in form-container-wide">
                            <form onSubmit={handleCreateAgreement}>
                                <div className="form-header-row">
                                    <h2 className="form-title">Service Agreement Intake</h2>
                                    <div className="invoice-date">Date: {formData.agreement_date}</div>
                                </div>

                                {/* Section 1 */}
                                <div className="section-divider">
                                    <span className="section-label">1. Responsible Party (Payer)</span>
                                </div>
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

                                {/* Section 2 */}
                                <div className="section-divider">
                                    <span className="section-label">2. Care Recipient</span>
                                </div>
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

                                {/* Section 3  */}
                                <div className="section-divider">
                                    <span className="section-label">3. Office Administration & Schedule</span>
                                </div>
                                <div className="admin-row-grid">
                                    <div className="form-group">
                                        <label>Initial Inquiry Date</label>
                                        <input type="date" name="initial_inquiry_date" className="form-input" value={formData.initial_inquiry_date} onChange={handleChange} />
                                    </div>
                                    <div className="form-group">
                                        <label>Instructions Given By</label>
                                        <input name="instructions_given_by" className="form-input" value={formData.instructions_given_by} onChange={handleChange} placeholder="Full Name" />
                                    </div>
                                    <div className="form-group">
                                        <label>Services Start Time</label>
                                        <input name="services_start_time" className="form-input" value={formData.services_start_time} onChange={handleChange} placeholder="e.g. 12:00 PM" />
                                    </div>
                                </div>

                                {/* Section 3 - Row 2 */}
                                <div className="admin-row-grid" style={{ marginTop: '20px' }}>
                                    <div className="form-group">
                                        <BranchDropdown onBranchChange={handleBranchSelect} selectedValue={formData.branch_code} />
                                    </div>
                                    <div className="form-group">
                                        <label>Handled By (Staff)</label>
                                        <input name="handled_by" className="form-input" value={formData.handled_by} onChange={handleChange} required />
                                    </div>
                                    <div className="form-group">
                                        <label>Hourly Rate ($)</label>
                                        <input name="hourly_rate" type="number" step="0.01" className="form-input" value={formData.hourly_rate} onChange={handleChange} />
                                    </div>
                                </div>

                                {/* Signature Section */}
                                <div className="signature-section-container">
                                    <label className="sig-label">Authorized Client Signature</label>
                                    <div className="signature-canvas-wrapper">
                                        <SignatureCanvas 
                                            ref={sigCanvas}
                                            penColor='#1e3a8a'
                                            canvasProps={{ className: 'sigCanvas_element' }} 
                                        />
                                    </div>
                                    <button type="button" onClick={clearSignature} className="clear-sig-btn">Clear Signature</button>
                                </div>

                                <div className="form-actions-row">
                                    <button type="submit" className="action-btn submit-flex" disabled={isGenerating}>
                                        {isGenerating ? "Processing..." : "Submit Agreement"}
                                    </button>
                                    <button type="button" onClick={() => setShowForm(false)} className="cancel-btn">Cancel</button>
                                </div>
                            </form>
                        </div>
                    ) : (
                        <div className="dashboard-home animate-fade-in">
                             <div className="stats-grid">
                                <div className="glass-card stat-box">
                                    <span>Active Vault Files</span>
                                    <h2>{agreements.length}</h2>
                                </div>
                                <button className="action-btn" onClick={() => setShowForm(true)} style={{fontSize: '18px'}}>+ New Agreement</button>
                            </div>
                        </div>
                    )
                )}

                {activeTab === 'documents' && (
                    <div className="glass-card animate-fade-in" style={{padding: '0', overflow: 'hidden'}}>
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
                                        <td className="p-20">{ag.branch_code}</td>
                                        <td className="p-20">${ag.hourly_rate}/hr</td>
                                        <td className="p-20">
                                            <button onClick={() => downloadPDF(ag.id, ag.clt_last_name)} className="action-btn small">Download PDF</button>
                                        </td>
                                    </tr>
                                )) : (
                                    <tr><td colSpan="4" className="p-20 text-center">No agreements found.</td></tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
            </main>
        </div>
    );
};

export default Dashboard;