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

    // Reset form when modal opens/closes or editing branch changes
    useEffect(() => {
        if (isOpen) {
            if (editingBranch) {
                // Populate form with branch data for editing
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
                // Reset form for new branch
                resetForm();
                setBranchCreationSuccess(false);
            }
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
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
        
        // Clear error for this field when user starts typing
        if (errors[name]) {
            setErrors(prev => ({ ...prev, [name]: '' }));
        }
    };

    const validateForm = () => {
        const newErrors = {};
        
        // Branch code validation
        if (!formData.branch_code.trim()) {
            newErrors.branch_code = 'Branch code is required';
        } else if (!/^[a-z0-9_]+$/.test(formData.branch_code)) {
            newErrors.branch_code = 'Branch code must contain only lowercase letters, numbers, and underscores';
        }
        
        // Branch name validation
        if (!formData.branch_name.trim()) {
            newErrors.branch_name = 'Branch name is required';
        }
        
        // Street validation
        if (!formData.street.trim()) {
            newErrors.street = 'Street address is required';
        }
        
        // City validation
        if (!formData.city.trim()) {
            newErrors.city = 'City is required';
        }
        
        // State validation
        if (!formData.branch_state.trim()) {
            newErrors.branch_state = 'State is required';
        } else if (!/^[A-Z]{2}$/.test(formData.branch_state.toUpperCase())) {
            newErrors.branch_state = 'State must be 2 letters (e.g., MD, VA, GA)';
        }
        
        // ZIP code validation - accepts any format (US, international, etc.)
        if (!formData.zipcode.trim()) {
            newErrors.zipcode = 'ZIP code is required';
        }
        
        // Phone validation (optional but if provided, validate format)
        if (formData.branch_phone && !/^[\d\s\-\(\)]+$/.test(formData.branch_phone)) {
            newErrors.branch_phone = 'Invalid phone format';
        }
        
        // Mileage validation
        if (formData.mileage && (formData.mileage < 0 || formData.mileage > 10)) {
            newErrors.mileage = 'Mileage rate should be between 0 and 10';
        }
        
        return newErrors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validate form
        const newErrors = validateForm();
        if (Object.keys(newErrors).length > 0) {
            setErrors(newErrors);
            return;
        }
        
        setLoading(true);
        
        try {
            // Determine if creating or updating
            const url = editingBranch 
                ? `${endpoint}/branches/${formData.branch_code}`
                : `${endpoint}/branches`;
            
            const method = editingBranch ? 'PUT' : 'POST';
            
            // Prepare data - convert state to uppercase
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
                    // New branch created - store the code and show copy modal
                    setNewBranchCode(formData.branch_code);
                    setBranchCreationSuccess(true);
                    setShowCopyModal(true);
                    // Don't close the main modal yet
                } else {
                    // For editing, just refresh and close
                    alert('Branch updated successfully!');
                    onSave();
                    onClose();
                }
            } else {
                // Show error from server
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
        const message = results?.agreements > 0 
            ? `Branch created successfully!\n\nContent copied:\n• ${results.agreements} agreement settings\n• ${results.rates} rate settings`
            : 'Branch created successfully!';
        
        alert(message);
        setShowCopyModal(false);
        setBranchCreationSuccess(false);
        onSave(); // Refresh the branches list
        onClose(); // Close the branch modal
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
                                        disabled={!!editingBranch} // Can't edit code after creation
                                    />
                                    {errors.branch_code && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.branch_code}
                                        </div>
                                    )}
                                    {!editingBranch && (
                                        <small style={{color: '#64748b', fontSize: '11px'}}>
                                            Use lowercase letters, numbers, and underscores only
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
                                
                                {/* Mileage Rate */}
                                <div className="form-group">
                                    <label>Mileage Rate ($/mile)</label>
                                    <input
                                        type="number"
                                        name="mileage"
                                        value={formData.mileage}
                                        onChange={handleChange}
                                        step="0.01"
                                        min="0"
                                        max="10"
                                        className={`form-input ${errors.mileage ? 'input-error' : ''}`}
                                    />
                                    {errors.mileage && (
                                        <div className="error-text" style={{color: '#ef4444', fontSize: '12px', marginTop: '4px'}}>
                                            {errors.mileage}
                                        </div>
                                    )}
                                </div>
                                
                                {/* Checkboxes */}
                                <div className="form-group" style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
                                    <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <input
                                            type="checkbox"
                                            name="admin_meds"
                                            checked={formData.admin_meds}
                                            onChange={handleChange}
                                        />
                                        Admin Medications
                                    </label>
                                    
                                    <label style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                        <input
                                            type="checkbox"
                                            name="is_corporate"
                                            checked={formData.is_corporate}
                                            onChange={handleChange}
                                        />
                                        Corporate Branch
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <div className="modal-footer">
                            <button type="button" onClick={onClose} className="cancel-btn">
                                Cancel
                            </button>
                            <button type="submit" className="action-btn" disabled={loading}>
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