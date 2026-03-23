import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';
import BranchModal from "./BranchModal";
import BranchContentEditor from "./BranchContentEditor";
import CopyContentModal from "./CopyContentModal";

const BranchesList = ({ token, onBranchesChanged, onCreateAgreement }) => {
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showModal, setShowModal] = useState(false);
    const [editingBranch, setEditingBranch] = useState(null);
    const [initialLoadDone, setInitialLoadDone] = useState(false);
    
    // State variables for content editing and copying
    const [showContentEditor, setShowContentEditor] = useState(false);
    const [selectedBranchForContent, setSelectedBranchForContent] = useState(null);
    const [showCopyModal, setShowCopyModal] = useState(false);
    const [selectedBranchForCopy, setSelectedBranchForCopy] = useState(null);

    useEffect(() => {
        fetchBranches();
    }, [token]);

    const fetchBranches = async () => {
        setLoading(true);
        try {
            const response = await fetch(`${endpoint}/branches?t=${new Date().getTime()}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            setBranches(data);
            setError('');
            // Notify parent (Dashboard) to refresh its branch list, but skip on initial load
            if (initialLoadDone && onBranchesChanged) onBranchesChanged();
            setInitialLoadDone(true);
        } catch (err) {
            console.error("Error fetching branches:", err);
            setError('Failed to load branches');
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (branchCode, branchName) => {
        if (!window.confirm(`Are you sure you want to delete "${branchName}"? This action cannot be undone.`)) return;
        
        try {
            const response = await fetch(`${endpoint}/branches/${branchCode}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            
            if (response.ok) {
                fetchBranches();
            } else {
                const data = await response.json();
                alert(data.detail || 'Failed to delete branch');
            }
        } catch (error) {
            alert('Failed to connect to server');
        }
    };

    const handleEditContent = (branch) => {
        setSelectedBranchForContent(branch);
        setShowContentEditor(true);
    };

    const handleCopyContent = (branch) => {
        setSelectedBranchForCopy(branch);
        setShowCopyModal(true);
    };

    const handleCopyComplete = (results) => {
        const message = results?.agreements > 0 
            ? `Content copied successfully!\n• ${results.agreements} agreement settings\n• ${results.rates} rate settings`
            : 'Content copied successfully!';
        
        alert(message);
        setShowCopyModal(false);
        setSelectedBranchForCopy(null);
        fetchBranches();
    };

    if (loading) {
        return (
            <div style={{ 
                display: 'flex', 
                justifyContent: 'center', 
                alignItems: 'center', 
                height: '400px',
                color: '#64748b',
                fontSize: '1.1rem'
            }}>
                Loading branches...
            </div>
        );
    }

    return (
        <div style={{ 
            padding: '24px',
            maxWidth: '1200px',
            margin: '0 auto'
        }}>
            {/* Header Section */}
            <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                marginBottom: '32px'
            }}>
                <div>
                    <h1 style={{ 
                        margin: '0 0 8px 0', 
                        fontSize: '28px', 
                        fontWeight: '600',
                        color: '#0f172a'
                    }}>
                        All Branches
                    </h1>
                    <p style={{ 
                        margin: 0, 
                        color: '#64748b',
                        fontSize: '15px'
                    }}>
                        Manage branch information and agreement content
                    </p>
                </div>
                <button 
                    onClick={() => {
                        setEditingBranch(null);
                        setShowModal(true);
                    }}
                    style={{
                        padding: '12px 24px',
                        background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '10px',
                        fontSize: '15px',
                        fontWeight: '600',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        boxShadow: '0 4px 6px -1px rgba(79, 172, 254, 0.3)',
                        transition: 'transform 0.2s, box-shadow 0.2s'
                    }}
                    onMouseOver={(e) => {
                        e.target.style.transform = 'translateY(-1px)';
                        e.target.style.boxShadow = '0 6px 10px -1px rgba(79, 172, 254, 0.4)';
                    }}
                    onMouseOut={(e) => {
                        e.target.style.transform = 'translateY(0)';
                        e.target.style.boxShadow = '0 4px 6px -1px rgba(79, 172, 254, 0.3)';
                    }}
                >
                    <span style={{ fontSize: '20px' }}>+</span>
                    Add New Branch
                </button>
            </div>

            {error && (
                <div style={{ 
                    backgroundColor: '#fef2f2',
                    color: '#991b1b',
                    padding: '16px',
                    borderRadius: '10px',
                    marginBottom: '24px',
                    border: '1px solid #fecaca'
                }}>
                    {error}
                </div>
            )}

            {/* Branches Grid */}
            {branches.length === 0 ? (
                <div style={{ 
                    textAlign: 'center', 
                    padding: '60px 40px',
                    backgroundColor: '#f8fafc',
                    borderRadius: '16px',
                    border: '2px dashed #e2e8f0'
                }}>
                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>🏢</div>
                    <h3 style={{ 
                        margin: '0 0 8px 0', 
                        fontSize: '20px', 
                        fontWeight: '600',
                        color: '#0f172a'
                    }}>
                        No branches found
                    </h3>
                    <p style={{ 
                        margin: '0 0 24px 0', 
                        color: '#64748b',
                        fontSize: '15px'
                    }}>
                        Get started by creating your first branch
                    </p>
                    <button 
                        onClick={() => {
                            setEditingBranch(null);
                            setShowModal(true);
                        }}
                        style={{
                            padding: '12px 24px',
                            background: '#ffffff',
                            color: '#4facfe',
                            border: '2px solid #4facfe',
                            borderRadius: '10px',
                            fontSize: '15px',
                            fontWeight: '600',
                            cursor: 'pointer',
                            transition: 'all 0.2s'
                        }}
                        onMouseOver={(e) => {
                            e.target.style.background = '#4facfe';
                            e.target.style.color = 'white';
                        }}
                        onMouseOut={(e) => {
                            e.target.style.background = 'white';
                            e.target.style.color = '#4facfe';
                        }}
                    >
                        Create Your First Branch
                    </button>
                </div>
            ) : (
                <div style={{ 
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))',
                    gap: '20px'
                }}>
                    {branches.map(branch => (
                        <div key={branch.branch_code} style={{
                            backgroundColor: 'white',
                            borderRadius: '12px',
                            border: '1px solid #e2e8f0',
                            overflow: 'hidden',
                            transition: 'box-shadow 0.2s, transform 0.2s',
                            boxShadow: '0 2px 4px rgba(0,0,0,0.02)'
                        }}
                        onMouseOver={(e) => {
                            e.currentTarget.style.boxShadow = '0 10px 25px -5px rgba(0,0,0,0.1)';
                            e.currentTarget.style.transform = 'translateY(-2px)';
                        }}
                        onMouseOut={(e) => {
                            e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.02)';
                            e.currentTarget.style.transform = 'translateY(0)';
                        }}>
                            {/* Branch Header */}
                            <div style={{
                                padding: '16px 20px',
                                background: 'linear-gradient(135deg, #f8fafc 0%, #ffffff 100%)',
                                borderBottom: '1px solid #e2e8f0'
                            }}>
                                <h3 style={{
                                    margin: '0 0 4px 0',
                                    fontSize: '18px',
                                    fontWeight: '600',
                                    color: '#0f172a'
                                }}>
                                    {branch.branch_name}
                                </h3>
                                <p style={{
                                    margin: 0,
                                    fontSize: '13px',
                                    color: '#4facfe',
                                    fontFamily: 'monospace'
                                }}>
                                    {branch.branch_code}
                                </p>
                            </div>

                            {/* Branch Details */}
                            <div style={{ padding: '16px 20px' }}>
                                <div style={{ 
                                    display: 'flex', 
                                    alignItems: 'center',
                                    gap: '8px',
                                    marginBottom: '8px',
                                    color: '#334155'
                                }}>
                                    <span style={{ fontSize: '16px' }}>📍</span>
                                    <span style={{ fontSize: '14px' }}>
                                        {[branch.street, branch.city, branch.branch_state, branch.zipcode]
                                            .filter(Boolean)
                                            .join(', ') || 'Address not provided'}
                                    </span>
                                </div>
                                
                                {branch.branch_phone && (
                                    <div style={{ 
                                        display: 'flex', 
                                        alignItems: 'center',
                                        gap: '8px',
                                        marginBottom: '8px',
                                        color: '#334155'
                                    }}>
                                        <span style={{ fontSize: '16px' }}>📞</span>
                                        <span style={{ fontSize: '14px' }}>{branch.branch_phone}</span>
                                    </div>
                                )}
                                
                                <div style={{ 
                                    display: 'flex', 
                                    alignItems: 'center',
                                    gap: '8px',
                                    marginBottom: '8px',
                                    color: '#334155'
                                }}>
                                    {/* <span style={{ fontSize: '16px' }}>💰</span>
                                    <span style={{ fontSize: '14px' }}>
                                        Mileage: ${branch.mileage?.toFixed(2) || '0.67'}/mile
                                    </span> */}
                                </div>
                            </div>

                            {/* Action Buttons - Three buttons */}
                            <div style={{
                                padding: '16px 20px',
                                background: '#f8fafc',
                                borderTop: '1px solid #e2e8f0',
                                display: 'grid',
                                gridTemplateColumns: '1fr 1fr 1fr',
                                gap: '8px'
                            }}>
                                {/* Edit Content Button */}
                                <button 
                                    onClick={() => handleEditContent(branch)}
                                    style={{
                                        padding: '8px 0',
                                        background: 'white',
                                        color: '#4facfe',
                                        border: '1px solid #4facfe',
                                        borderRadius: '6px',
                                        fontSize: '13px',
                                        fontWeight: '500',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                    onMouseOver={(e) => {
                                        e.target.style.background = '#4facfe';
                                        e.target.style.color = 'white';
                                    }}
                                    onMouseOut={(e) => {
                                        e.target.style.background = 'white';
                                        e.target.style.color = '#4facfe';
                                    }}
                                    title="Edit agreement content for this branch"
                                >
                                    Edit Content
                                </button>

                                {/* Edit Branch Info Button */}
                                <button 
                                    onClick={() => {
                                        setEditingBranch(branch);
                                        setShowModal(true);
                                    }}
                                    style={{
                                        padding: '8px 0',
                                        background: 'white',
                                        color: '#f59e0b',
                                        border: '1px solid #f59e0b',
                                        borderRadius: '6px',
                                        fontSize: '13px',
                                        fontWeight: '500',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                    onMouseOver={(e) => {
                                        e.target.style.background = '#f59e0b';
                                        e.target.style.color = 'white';
                                    }}
                                    onMouseOut={(e) => {
                                        e.target.style.background = 'white';
                                        e.target.style.color = '#f59e0b';
                                    }}
                                    title="Edit branch information"
                                >
                                    Edit Info
                                </button>

                                {/* Copy Content Button */}
                                <button 
                                    onClick={() => handleCopyContent(branch)}
                                    style={{
                                        padding: '8px 0',
                                        background: 'white',
                                        color: '#8b5cf6',
                                        border: '1px solid #8b5cf6',
                                        borderRadius: '6px',
                                        fontSize: '13px',
                                        fontWeight: '500',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                    onMouseOver={(e) => {
                                        e.target.style.background = '#8b5cf6';
                                        e.target.style.color = 'white';
                                    }}
                                    onMouseOut={(e) => {
                                        e.target.style.background = 'white';
                                        e.target.style.color = '#8b5cf6';
                                    }}
                                    title="Copy content from this branch to another"
                                >
                                    Copy From
                                </button>
                            </div>

                            {/* Delete Button and Create Agreement - Separate row */}
                            <div style={{
                                padding: '0 20px 16px 20px',
                                background: '#f8fafc',
                                display: 'flex',
                                gap: '8px'
                            }}>
                                {/* Create Agreement Button */}
                                {onCreateAgreement && (
                                    <button 
                                        onClick={() => onCreateAgreement(branch.branch_code)}
                                        style={{
                                            flex: 1,
                                            padding: '8px 0',
                                            background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                                            color: 'white',
                                            border: 'none',
                                            borderRadius: '6px',
                                            fontSize: '13px',
                                            fontWeight: '500',
                                            cursor: 'pointer',
                                            transition: 'opacity 0.2s'
                                        }}
                                        onMouseOver={(e) => e.target.style.opacity = '0.85'}
                                        onMouseOut={(e) => e.target.style.opacity = '1'}
                                        title="Create a new agreement using this branch"
                                    >
                                        + New Agreement
                                    </button>
                                )}
                                <button 
                                    onClick={() => handleDelete(branch.branch_code, branch.branch_name)}
                                    style={{
                                        flex: 1,
                                        padding: '8px 0',
                                        background: 'white',
                                        color: '#ef4444',
                                        border: '1px solid #ef4444',
                                        borderRadius: '6px',
                                        fontSize: '13px',
                                        fontWeight: '500',
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                    onMouseOver={(e) => {
                                        e.target.style.background = '#ef4444';
                                        e.target.style.color = 'white';
                                    }}
                                    onMouseOut={(e) => {
                                        e.target.style.background = 'white';
                                        e.target.style.color = '#ef4444';
                                    }}
                                    title="Delete this branch (cannot be undone)"
                                >
                                    Delete Branch
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Branch Modal (Create/Edit Branch Info) */}
            <BranchModal
                isOpen={showModal}
                onClose={() => {
                    setShowModal(false);
                    setEditingBranch(null);
                }}
                onSave={fetchBranches}
                token={token}
                endpoint={endpoint}
                editingBranch={editingBranch}
            />

            {/* Branch Content Editor Modal */}
            <BranchContentEditor
                isOpen={showContentEditor}
                onClose={() => {
                    setShowContentEditor(false);
                    setSelectedBranchForContent(null);
                }}
                onSave={() => {
                    setShowContentEditor(false);
                    setSelectedBranchForContent(null);
                }}
                token={token}
                branchCode={selectedBranchForContent?.branch_code}
                branchName={selectedBranchForContent?.branch_name}
            />

            {/* Copy Content Modal */}
            <CopyContentModal
                isOpen={showCopyModal}
                onClose={() => {
                    setShowCopyModal(false);
                    setSelectedBranchForCopy(null);
                }}
                onCopy={handleCopyComplete}
                token={token}
                currentBranchCode={selectedBranchForCopy?.branch_code}
                branchName={selectedBranchForCopy?.branch_name}
            />
        </div>
    );
};

export default BranchesList;