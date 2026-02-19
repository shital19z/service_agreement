import React, { useState, useEffect } from 'react';

const BranchDropdown = ({ onBranchChange, selectedValue }) => {
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchBranches = async () => {
            try {
                setLoading(true);
                // Added a timestamp to the URL to prevent browser caching (the 24 vs 70 issue)
                const response = await fetch(`http://127.0.0.1:8000/branches?t=${new Date().getTime()}`);
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const data = await response.json();
                console.log("Branches received by component:", data);
                setBranches(data);
            } catch (err) {
                console.error("Error loading branches:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchBranches();
    }, []);

    const handleSelect = (e) => {
        const selectedCode = e.target.value;
        const branchObj = branches.find(b => b.branch_code === selectedCode);
        
        if (branchObj) {
            console.log("Selected branch object:", branchObj);
            onBranchChange({
                branch_code: branchObj.branch_code,
                branch_name: branchObj.branch_name,
                // Match the backend key 'branch_state'
                state_code: branchObj.branch_state || 'MD' 
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