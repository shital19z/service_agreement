import React, { useState, useEffect } from 'react';
import { endpoint } from '../resource/Constant';

const BranchDropdown = ({ onBranchChange, selectedValue, branches: externalBranches, loading: externalLoading }) => {
    const [internalBranches, setInternalBranches] = useState([]);
    const [internalLoading, setInternalLoading] = useState(true);
    const [error, setError] = useState(null);

    // Use external branches if provided, otherwise fetch internally
    const branches = externalBranches || internalBranches;
    const loading = externalBranches ? (externalLoading || false) : internalLoading;

    useEffect(() => {
        // Only fetch internally if no external branches are provided
        if (externalBranches) return;

        const fetchBranches = async () => {
            try {
                setInternalLoading(true);
                const response = await fetch(`${endpoint}/branches?t=${new Date().getTime()}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                setInternalBranches(data);
            } catch (err) {
                console.error("Error loading branches:", err);
                setError(err.message);
            } finally {
                setInternalLoading(false);
            }
        };

        fetchBranches();
    }, [externalBranches]);

    const handleSelect = (e) => {
        const selectedCode = e.target.value;
        const branchObj = branches.find(b => b.branch_code === selectedCode);
        
        if (branchObj) {
            onBranchChange({
                branch_code: branchObj.branch_code,
                branch_name: branchObj.branch_name,
                state_code: branchObj.branch_state
            });
        } else {
            onBranchChange(null);
        }
    };

    if (error) {
        return <p style={{ color: '#ef4444' }}>Error loading branches: {error}</p>;
    }

    return (
        <div className="form-group">
            <label style={{ fontWeight: 'bold', marginBottom: '5px', display: 'block' }}>
                Office Branch <span style={{ color: '#ef4444' }}>*</span>
            </label>
            
            <select 
                className="form-input" 
                value={selectedValue || ""}
                onChange={handleSelect}
                required
                style={{
                    width: '100%',
                    padding: '8px',
                    borderRadius: '4px',
                    border: '1px solid #ccc',
                    color: '#000', // Ensures text isn't white-on-white
                    backgroundColor: '#fff'
                }}
            >
                <option value="">
                    {loading ? "Loading branches..." : "-- Select Branch --"}
                </option>
                
                {branches.map((branch) => (
                    <option 
                        key={branch.branch_code} 
                        value={branch.branch_code}
                    >
                        {/* Fallback to code if name is missing */}
                        {branch.branch_name || branch.branch_code}
                    </option>
                ))}
            </select>

            {branches.length === 0 && !loading && (
                <p style={{ color: '#ef4444', fontSize: '12px', marginTop: '5px' }}>
                    No branches found. Please check your database connection.
                </p>
            )}
        </div>
    );
};

export default BranchDropdown;