import React, { useState, useEffect } from 'react';

const BranchDropdown = ({ onBranchChange, selectedValue }) => {
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
    const fetchBranches = async () => {
        try {
            setLoading(true);
            const response = await fetch('http://127.0.0.1:8000/branches');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("Branches received:", data);
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
            console.log("Selected branch:", branchObj); // Debug log
            onBranchChange({
                branch_code: branchObj.branch_code,
                branch_name: branchObj.branch_name,
                state_code: branchObj.state_code
            });
        }
    };

    return (
        <div className="form-group">
            <label>Office Branch <span style={{color: '#ef4444'}}>*</span></label>
            <select 
                className="form-input" 
                value={selectedValue || ""}
                onChange={handleSelect}
                required
            >
                <option value="">
                    {loading ? "Loading branches..." : "-- Select Branch --"}
                </option>
                {branches.map((branch) => (
                    <option key={branch.branch_code} value={branch.branch_code}>
                        {branch.branch_name}
                    </option>
                ))}
            </select>
            {branches.length === 0 && !loading && (
                <p style={{color: '#ef4444', fontSize: '12px', marginTop: '5px'}}>
                    No branches found. Please check server connection.
                </p>
            )}
        </div>
    );
};

export default BranchDropdown;