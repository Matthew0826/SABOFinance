import React, { useState, useEffect } from 'react';

const ApprovedRequest = ({ curr_req, sortedEntries, req_list, user, postApproval, postFiles }) => {
    const [cost, setCost] = useState(0);  // Default to approved
    const [tax, setTax] = useState(0);
    const [files, setFiles] = useState([]);

    const handleFileChange = (e) => {

        const maxSize = 1 * 1024 * 1024; // 1 MB
        const selectedFiles = Array.from(e.target.files);

        // Filter out files that exceed the size limit
        const validFiles = selectedFiles.filter(file => file.size <= maxSize);

        if (validFiles.length < selectedFiles.length) {
            alert('File exceeds size limit of 1 MB.');
        } else {
            if (e.target.files.length > 0) {
                setFiles([...files, ...Array.from(e.target.files)]);
            }
        }
    };

    useEffect(() => {
        try {
            setCost(req_list[curr_req]["Requested Cost"])
        } catch { setCost(0) }
    }, [curr_req]);

    const removeFile = (index) => {
        const newFiles = files.filter((file, i) => i !== index);
        setFiles(newFiles);
    };

    const canApprove = (user, request) => {
        console.log(user["Permissions"])
        var is_business = (user["Permissions"].includes("Business") && request["Status"] === "Pending Approval")
        var is_admin = (user["Permissions"].includes("Admin") && user["Permissions"].includes(request["Project"]) && request["Status"] === "Pending Approval")
        return is_business || is_admin
    }

    return (
        <div>
            {curr_req >= 0 && sortedEntries[curr_req] && req_list[curr_req]["Status"] === 'Approved' ? (
                <>
                    {/* Render details of the currently selected request */}
                    At {req_list[curr_req]["Request Date"]} you requested:
                    <br />
                    <b>{req_list[curr_req]["Description"]}</b><br />
                    <b>Approved Cost: ${req_list[curr_req]["Requested Cost"]}</b>
                    <br />
                    <a href={req_list[curr_req]["Link"]} target="_blank" rel="noopener noreferrer">Link</a>
                    <br /><br />
                    <b>Status: {req_list[curr_req]["Status"]}</b><br />
                    Final Cost (No Tax): $<input value={cost} onChange={
                        (event) => {
                            console.log(event.target.value + ", " + req_list[curr_req]["Requested Cost"])
                            if (parseFloat(event.target.value) <= parseFloat(req_list[curr_req]["Requested Cost"])) {
                                console.log("test"); setCost(event.target.value)
                            }
                        }} className="input" type="number" step="0.01" />
                    <br />
                    Tax: $<input value={tax} onChange={(e) => { setTax(e.target.value) }} className="input" type="number" step="0.01" />
                    <br />
                    {files.length < 7 && (
                        <input
                            type="file"
                            onChange={handleFileChange}
                            accept=".gif, .png, .pdf, .jpg"
                            multiple
                        />
                    )}
                    {files.map((file, index) => (
                        <ul key={index}>
                            {file.name}&nbsp;&nbsp;
                            <button onClick={() => removeFile(index)}>Remove</button>
                        </ul>
                    ))}
                    <br />
                    <button onClick={() => postFiles(cost, tax, req_list[curr_req], curr_req, files)}>Submit</button>
                </>
            ) : (
                <></>
            )}
        </div>
    );
};

export default ApprovedRequest;