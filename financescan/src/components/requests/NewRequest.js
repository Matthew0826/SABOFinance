import React, { useState, useEffect } from 'react';

const NewRequest = ({ curr_req, setCurrReq, options, user, postRequest }) => {
    const [index, setIndex] = useState(''); // State to store selected account type
    const [description, setDescription] = useState(''); // State to store description input
    const [cost, setCost] = useState(0); // State to store requested cost input
    const [link, setLink] = useState(''); // State to store link input
    const [accountOptions, setAccountOptions] = useState([]); // State for managing account options

    // Various states to manage form inputs and selections
    const [account, setAccount] = useState(''); // State to store selected account option
    const [project, setProject] = useState(user["Project"]); // State to store project selected from user prop
    const [subteam, setSubteam] = useState(user["Subteam"]); // State to store selected subteam

    // Get project and subteam options from passed options prop
    const currProjects = options["Project Options"] || [];
    const subteamOptions = options["Subteam Options"] || [];

    const currSubteams = subteamOptions
        .filter(item => item.includes("(" + project + ")"))
        .map(item => item.replace("(" + project + ") ", ""));

    // Effect to update account options based on the selected account type (Budget or Cash)
    useEffect(() => {
        setAccountOptions(index === "Budget Account" ? options["Budget Account Options"] || [] : []);
    }, [index, options]); // Re-run effect when 'index' or 'options' change


    useEffect(() => {
        setAccountOptions(index === "Budget Account" ? options["Budget Account Options"] || [] : []);
    }, [index, options]); // Re-run effect when 'index' or 'options' change

    // Effect to set the account value based on available account options
    useEffect(() => {
        setAccount(accountOptions[0] || '');
    }, [accountOptions]);


    // Effect to update subteam and project when the 'user' prop changes
    useEffect(() => {
        if (user && user["Subteam"]) {
            setSubteam(user["Subteam"].replace(`(${project}) `, "")); // Update subteam after removing project info
            setProject(user["Project"]); // Set project based on the 'user' prop
            setIndex("Budget Account"); // Default to 'Budget Account' option
        }
    }, [user]); // Effect re-runs when 'user' changes

    useEffect(() => {
        setSubteam(currSubteams[0] || "")
    }, [project]);

    //When the account is selected
    const onAccountSelect = (event) => {
        setIndex(event.target.value);
        if (event.target.value === "Cash Account") {
            setAccountOptions([]); // Clear account options if Cash Account is selected
        } else {
            setAccountOptions(options["Budget Account Options"]); // Set options for Budget Account
        }
    }

    // Function to submit a new request to the server
    const sendRequest = () => {
        // Ensure all necessary fields are filled
        if (description === '' || link === '' || cost === 0) {
            return;
        }

        // Call the postRequest function passed as a prop with form data
        postRequest({
            'Requestee': user['Name'], 'Index': index, 'Account': account,
            'Description': description, 'Project': project, 'Subteam': subteam, 'Cost': cost, 'Link': link
        });

        setCurrReq(-1); // Reset the current request
    };

    return (
        <div className={curr_req !== -2 ? "disabled" : "curr_content"}>

            {/* Account type selection */}
            <select value={index} onChange={(event) => onAccountSelect(event)}>
                <option value="Budget Account">Budget Account</option>
                <option value="Cash Account">Cash Account</option>
            </select>&nbsp;&nbsp;&nbsp;&nbsp;

            {/* Account options selection */}
            <select value={account} onChange={(event) => setAccount(event.target.value)}>
                {accountOptions.map((opt, index) => (
                    <option key={index} value={opt}>{opt}</option>
                ))}
            </select>
            <br /><br />

            {/* Description input */}
            Description:&nbsp;
            <textarea
                className="input"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <br /><br />

            {/* Project selection */}
            Project:&nbsp;
            <select value={project} onChange={(event) => setProject(event.target.value)}>
                {currProjects.map((proj, index) => (
                    <option key={index} value={proj}>{proj}</option>
                ))}
            </select>
            <br /><br />

            {/* Subteam selection */}
            Subteam:&nbsp;
            <select value={subteam} onChange={(event) => setSubteam(event.target.value)}>
                {currSubteams.map((sbtm, index) => (
                    <option key={index} value={sbtm}>{sbtm}</option>
                ))}
            </select>
            <br /><br />

            {/* Requested cost input */}
            Requested Amount (No Tax):<br />$
            <input value={cost} onChange={(event) => setCost(event.target.value)} className="input" type="number" step="0.01" />
            <br /><br />

            {/* Link input */}
            Link:&nbsp;
            <textarea value={link} onChange={(event) => setLink(event.target.value)} />
            <br /><br />

            {/* Submit button for the request form */}
            <button className="submit_btn" onClick={sendRequest}>Submit</button>
        </div>
    );
};

export default NewRequest;
