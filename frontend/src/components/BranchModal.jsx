import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';
import CopyContentModal from './CopyContentModal';

const BranchModal = ({ isOpen, onClose, onSave, token, editingBranch = null }) => {
    const [formData, setFormData] = useState({
        branch_code: '',
        branch_name: '',
        office_name: 'Options For Senior America',
        street: '',
        city: '',
        branch_state: '',
        zipcode: '',
        branch_phone: '',
        branch_fax: '',
        mileage: 0.67,
        admin_meds: false,
        is_corporate: false,
    });
    
    const [errors, setErrors] = useState({});
    const [loading, setLoading] = useState(false);
    const [showCopyModal, setShowCopyModal] = useState(false);
    const [newBranchCode, setNewBranchCode] = useState('');
    const [branchCreationSuccess, setBranchCreationSuccess] = useState(false);

    useEffect(() => {
        if (isOpen) {
            if (editingBranch) {
                setFormData({
                    branch_code: editingBranch.branch_code || '',
                    branch_name: editingBranch.branch_name || '',
                    office_name: editingBranch.office_name || 'Options For Senior America',
                    street: editingBranch.street || '',
                    city: editingBranch.city || '',
                    branch_state: editingBranch.branch_state || '',
                    zipcode: editingBranch.zipcode || '',
                    branch_phone: editingBranch.branch_phone || '',
                    branch_fax: editingBranch.branch_fax || '',
                    mileage: editingBranch.mileage || 0.67,
                    admin_meds: editingBranch.admin_meds || false,
                    is_corporate: editingBranch.is_corporate || false
                });
                setBranchCreationSuccess(false);
            } else {
                resetForm();
                setBranchCreationSuccess(false);
            }
            setShowCopyModal(false);
        }
    }, [isOpen, editingBranch]);

    const resetForm = () => {
        setFormData({
            branch_code: '',
            branch_name: '',
            office_name: 'Options For Senior America',
            street: '',
            city: '',
            branch_state: '',
            zipcode: '',
            branch_phone: '',
            branch_fax: '',
            mileage: 0.67,
            admin_meds: false,
            is_corporate: false
        });
        setErrors({});
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        
        let processedValue = value;
        if (name === 'branch_code' && !editingBranch) {
            processedValue = value.toLowerCase().replace(/[^a-z0-9_]/g, '');
        }
        
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : processedValue
        }));
        
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        
        if (!formData.branch_code.trim()) {
            newErrors.branch_code = 'Branch code is required';
        } else if (!/^[a-z0-9_]+$/.test(formData.branch_code)) {
            newErrors.branch_code = 'Branch code must contain only lowercase letters, numbers, and underscores';
        }
        
        if (!formData.branch_name.trim()) {
            newErrors.branch_name = 'Branch name is required';
        }
        
        if (!formData.street.trim()) {
            newErrors.street = 'Street address is required';
        }
        
        if (!formData.city.trim()) {
            newErrors.city = 'City is required';
        }
        
        if (!formData.branch_state.trim()) {
            newErrors.branch_state = 'State is required';
        } else if (!/^[A-Z]{2}$/.test(formData.branch_state.toUpperCase())) {
            newErrors.branch_state = 'State must be 2 letters (e.g., MD, VA, GA)';
        }
        
        if (!formData.zipcode.trim()) {
            newErrors.zipcode = 'ZIP code is required';
        }
        
        if (formData.branch_phone && !/^[\d\s\-\(\)]+$/.test(formData.branch_phone)) {
            newErrors.branch_phone = 'Invalid phone format';
        }
        
        return newErrors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const newErrors = validateForm();
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }
        
        setLoading(true);
        
        try {
            const url = editingBranch 
                ? `${endpoint}/branches/${formData.branch_code}`
                : `${endpoint}/branches`;
            
            const method = editingBranch ? 'PUT' : 'POST';
            
            const submitData = {
                ...formData,
                branch_state: formData.branch_state.toUpperCase()
            };
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(submitData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                if (!editingBranch) {
                    setNewBranchCode(formData.branch_code);
                    setBranchCreationSuccess(true);
                    setShowCopyModal(true);
                } else {
                    alert('Branch updated successfully!');
                    onSave();
                    onClose();
                }
            } else {
                alert(data.detail || 'Failed to save branch');
            }
        } catch (error) {
            console.error('Error saving branch:', error);
            alert('Failed to connect to server');
        } finally {
            setLoading(false);
        }
    };

    const handleCopyComplete = (results) => {
        const copiedItems = [];
        if (results?.agreements > 0) copiedItems.push('✓ Agreement settings');
        if (results?.rates > 0) copiedItems.push('✓ Rate settings');
        if (results?.services > 0) copiedItems.push('✓ Service settings');
        
        const message = copiedItems.length > 0 
            ? `Branch created successfully!\n\nContent copied:\n${copiedItems.join('\n')}`
            : 'Branch created successfully!';
        
        alert(message);
        
        setShowCopyModal(false);
        setBranchCreationSuccess(false);
        onSave();
        onClose();
    };

    const handleSkipCopy = () => {
        alert('Branch created successfully!');
        setShowCopyModal(false);
        setBranchCreationSuccess(false);
        onSave();
        onClose();
    };

    if (!isOpen) return null;

    return (
        <>
            <div className="modal-overlay">
                <div className="modal-content branch-modal" style={{ maxWidth: '600px' }}>
                    <div className="modal-header">
                        <h3>{editingBranch ? 'Edit Branch' : 'Add New Branch'}</h3>
                        <button onClick={onClose} className="modal-close">&times;</button>
                    </div>
                    
                    <form onSubmit={handleSubmit}>
                        <div className="modal-body">
                            <div className="form-grid-2">
                                {/* Branch Code */}
                                <div className="form-group">
                                    <label>Branch Code *</label>
                                    <input
                                        type="text"
                                        name="branch_code"
                                        value={formData.branch_code}
                                        onChange={handleChange}
                                        className={`form-input ${errors.branch_code ? 'input-error' : ''}`}
                                        placeholder="e.g., nyhomecare"
                                        disabled={!!editingBranch}
                                        style={{ 
                                            backgroundColor: editingBranch ? '#f5f5f5' : 'white',
                                            textTransform: 'lowercase'
                                        }}
                                    />
                                    {errors.branch_code && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.branch_code}
                                        </div>
                                    )}
                                    {!editingBranch && (
                                        <small style={{color: '#64748b', fontSize: '11px'}}>
                                            Auto-formatted: lowercase letters, numbers, underscores only
                                        </small>
                                    )}
                                </div>
                                
                                {/* Branch Name */}
                                <div className="form-group">
                                    <label>Branch Name *</label>
                                    <input
                                        type="text"
                                        name="branch_name"
                                        value={formData.branch_name}
                                        onChange={handleChange}
                                        className={`form-input ${errors.branch_name ? 'input-error' : ''}`}
                                        placeholder="e.g., New York Home Care"
                                    />
                                    {errors.branch_name && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.branch_name}
                                        </div>
                                    )}
                                </div>
                                
                                {/* Office Name */}
                                <div className="form-group span-2">
                                    <label>Office Name</label>
                                    <input
                                        type="text"
                                        name="office_name"
                                        value={formData.office_name}
                                        onChange={handleChange}
                                        className="form-input"
                                        placeholder="Options For Senior America"
                                    />
                                </div>
                                
                                {/* Street Address */}
                                <div className="form-group span-2">
                                    <label>Street Address *</label>
                                    <input
                                        type="text"
                                        name="street"
                                        value={formData.street}
                                        onChange={handleChange}
                                        className={`form-input ${errors.street ? 'input-error' : ''}`}
                                        placeholder="123 Main Street"
                                    />
                                    {errors.street && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.street}
                                        </div>
                                    )}
                                </div>
                                
                                {/* City */}
                                <div className="form-group">
                                    <label>City *</label>
                                    <input
                                        type="text"
                                        name="city"
                                        value={formData.city}
                                        onChange={handleChange}
                                        className={`form-input ${errors.city ? 'input-error' : ''}`}
                                    />
                                    {errors.city && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.city}
                                        </div>
                                    )}
                                </div>
                                
                                {/* State */}
                                <div className="form-group">
                                    <label>State *</label>
                                    <input
                                        type="text"
                                        name="branch_state"
                                        value={formData.branch_state}
                                        onChange={handleChange}
                                        className={`form-input ${errors.branch_state ? 'input-error' : ''}`}
                                        placeholder="MD"
                                        maxLength="2"
                                        style={{ textTransform: 'uppercase' }}
                                    />
                                    {errors.branch_state && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.branch_state}
                                        </div>
                                    )}
                                </div>
                                
                                {/* ZIP Code */}
                                <div className="form-group">
                                    <label>ZIP Code *</label>
                                    <input
                                        type="text"
                                        name="zipcode"
                                        value={formData.zipcode}
                                        onChange={handleChange}
                                        className={`form-input ${errors.zipcode ? 'input-error' : ''}`}
                                        placeholder="12345"
                                    />
                                    {errors.zipcode && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.zipcode}
                                        </div>
                                    )}
                                </div>
                                
                                {/* Phone */}
                                <div className="form-group">
                                    <label>Phone</label>
                                    <input
                                        type="text"
                                        name="branch_phone"
                                        value={formData.branch_phone}
                                        onChange={handleChange}
                                        className={`form-input ${errors.branch_phone ? 'input-error' : ''}`}
                                        placeholder="(555) 123-4567"
                                    />
                                    {errors.branch_phone && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.branch_phone}
                                        </div>
                                    )}
                                </div>
                                
                                {/* Fax */}
                                <div className="form-group">
                                    <label>Fax</label>
                                    <input
                                        type="text"
                                        name="branch_fax"
                                        value={formData.branch_fax}
                                        onChange={handleChange}
                                        className="form-input"
                                    />
                                </div>
                            </div>
                        </div>
                        
                        <div className="modal-footer" style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end', padding: '16px 24px', borderTop: '1px solid #e2e8f0' }}>
                            <button
                                type="button"
                                onClick={onClose}
                                style={{
                                    padding: '10px 24px',
                                    borderRadius: '8px',
                                    border: '1.5px solid #cbd5e1',
                                    backgroundColor: 'white',
                                    color: '#475569',
                                    fontSize: '14px',
                                    fontWeight: '500',
                                    cursor: 'pointer',
                                }}
                                onMouseOver={e => { e.target.style.backgroundColor = '#f8fafc'; e.target.style.borderColor = '#94a3b8'; }}
                                onMouseOut={e => { e.target.style.backgroundColor = 'white'; e.target.style.borderColor = '#cbd5e1'; }}
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                disabled={loading}
                                style={{
                                    padding: '10px 28px',
                                    borderRadius: '8px',
                                    border: 'none',
                                    background: loading ? '#94a3b8' : 'linear-gradient(135deg, #3b82f6, #2563eb)',
                                    color: 'white',
                                    fontSize: '14px',
                                    fontWeight: '600',
                                    cursor: loading ? 'not-allowed' : 'pointer',
                                    boxShadow: loading ? 'none' : '0 2px 8px rgba(37, 99, 235, 0.35)',
                                }}
                                onMouseOver={e => { if (!loading) { e.target.style.background = 'linear-gradient(135deg, #2563eb, #1d4ed8)'; e.target.style.boxShadow = '0 4px 12px rgba(37, 99, 235, 0.45)'; }}}
                                onMouseOut={e => { if (!loading) { e.target.style.background = 'linear-gradient(135deg, #3b82f6, #2563eb)'; e.target.style.boxShadow = '0 2px 8px rgba(37, 99, 235, 0.35)'; }}}
                            >
                                {loading ? 'Saving...' : (editingBranch ? 'Update Branch' : 'Create Branch')}
                            </button>
                        </div>
                    </form>
                </div>
            </div>

            {/* Copy Content Modal - Only show for new branches */}
            {!editingBranch && (
                <CopyContentModal
                    isOpen={showCopyModal}
                    onClose={handleSkipCopy}
                    onCopy={handleCopyComplete}
                    token={token}
                    currentBranchCode={newBranchCode}
                    branchName={formData.branch_name}
                />
            )}
        </>
    );
};

export default BranchModal;