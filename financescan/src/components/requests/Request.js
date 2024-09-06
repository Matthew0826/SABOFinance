import React, { useState } from 'react';

const Request = ({ curr_req, sortedEntries, req_list, user, postApproval }) => {
    const [approved, setApproved] = useState(true);  // Default to approved
    const [note, setNote] = useState('');

    const approve = () => {
        postApproval({
            'approved': approved,
            'request': req_list[curr_req],
            'id': curr_req,
            'user': user,
            'note': note
        })
    }

    const canApprove = (user, request) => {
        console.log(user["Permissions"])
        var is_business = (user["Permissions"].includes("Business") && request["Status"] === "Pending Approval")
        var is_admin = (user["Permissions"].includes("Admin") && user["Permissions"].includes(request["Project"]) && request["Status"] === "Pending Approval")
        return is_business || is_admin
    }

    return (
        <div>
            {curr_req >= 0 && sortedEntries[curr_req] ? (
                <>
                    {/* Render details of the currently selected request */}
                    At {req_list[curr_req]["Request Date"]} from {req_list[curr_req]["Requestee"]}
                    <br /><br />
                    <b>{req_list[curr_req]["Description"]}</b><br />
                    <b>${req_list[curr_req]["Requested Cost"]}</b>
                    <br />
                    <a href={req_list[curr_req]["Link"]} target="_blank" rel="noopener noreferrer">Link</a>
                    <br /><br />
                    {req_list[curr_req]["Budget Index"]}<br />{req_list[curr_req]["Account"]}
                    <br /><br />
                    Project: {req_list[curr_req]["Project"]} <br />Subteam: {req_list[curr_req]["Subteam"]}
                    <br /><br />
                    <b>Status: {req_list[curr_req]["Status"]}</b><br />

                    {/* If user has 'Business' permissions and request is pending, display approval options */}
                    {canApprove(user, req_list[curr_req]) && (
                        <>
                            <hr />
                            {/* Approval select option */}
                            <select value={approved} onChange={(e) => setApproved(e.target.value === 'true')}>
                                <option value="true">Approve</option>
                                <option value="false">Deny</option>
                            </select>
                            {/* Conditional note input if the request is denied */}
                            {!approved && (
                                <>
                                    <br /><br />Note: <textarea value={note} onChange={(e) => setNote(e.target.value)} />
                                </>
                            )}
                            <br />
                            {/* Button to submit approval/denial */}
                            <button onClick={approve}>Submit</button>
                        </>
                    )}
                </>
            ) : (
                <span>No request selected</span>
            )}
        </div>
    );
};

export default Request;

