import React, { useState } from 'react';
import './MainPage.css'; // Import the CSS file

const InfoPage = ({ req_list, user, options }) => {
    // State to keep track of the currently selected request
    const [curr_req, setCurrReq] = useState(-1);
    // State to manage the description input field
    const [description, setDescription] = useState();
    // The current project that is selected
    const [project, setProject] = useState();
    // The current subteam selected
    const [subteam, setSubteam] = useState();


    // Function to get the background color for each item based on the current selection
    const getItemColor = (key) => {
        return key === curr_req ? 'grey' : 'lightgrey'; // Highlight the selected item
    };

    // Sort the request list entries in descending order by key
    const sortedEntries = Object.entries(req_list).sort(([keyA], [keyB]) => keyB.localeCompare(keyA));
    const currProjects = options["Project Options"] || []
    const subteamOptions = options["Subteam Options"] || []
    const currSubteams = subteamOptions.filter(item => item.includes("(" + project + ")")).map(item => item.replace("(" + project + ") ", ""))

    return (
        <div className="content">
            {/* Requests Section */}
            <div className="requests">
                <div className="scrollable-container">
                    {/* Map over the sorted entries to create a list of requests */}
                    {sortedEntries.map(([key, value], index) => (
                        <div
                            onClick={() => {
                                console.log('hi');
                                setCurrReq(key);
                            }}
                            className='item'
                            key={key}
                            style={{ backgroundColor: getItemColor(key) }}>
                            {key}: {value["Description"]}, Status: {value["Status"]}, Requested Cost: {value["Requested Cost"]}
                        </div>
                    ))}
                </div>
                {/* Button to submit a new request */}
                <button className="submit_btn" onClick={() => { setCurrReq(-2) }}>Add Request</button>
            </div>

            {/* Conditional rendering based on the currently selected request */}
            {/* If a request is selected, display its content */}
            <div className={curr_req >= 0 ? "curr_content" : "disabled"}>
                {curr_req}<br />Test
                {console.log(currProjects)}
            </div>

            {/* If the submit request button is clicked, show the submission form */}
            <div className={curr_req !== -2 ? "disabled" : "curr_content"}>
                <select>
                    <option value="test">Budget Account</option>
                    <option value="test">Cash Account</option>
                </select>
                <br /> <br />
                Description:&nbsp;
                <textarea
                    className="input"
                    value={description}
                    onChange={(e) => { setDescription(e.target.value) }}
                />
                <br /> <br />
                Project:&nbsp;
                <select value={project} onChange={(event) => setProject(event.target.value)}>
                    {currProjects.map((proj, index) => (
                        <option key={index} value={proj}>{proj}</option>
                    ))}
                </select>
                <br /> <br />
                Subteam:&nbsp;
                <select value={subteam} onChange={(event) => setSubteam(event.target.value)}>
                    {currSubteams.map((sbtm, index) => (
                        <option key={index} value={sbtm}>{sbtm}</option>
                    ))}
                </select>
                <br /> <br />
                Requested Amount (No Tax): <br></br>$
                <input className="input" type="number" step="0.01" />
                <br /> <br />
                Link:&nbsp;
                <textarea />
                <br /> <br />
                <button className="submit_btn">Submit</button>
            </div>
        </div>
    );
};

export default InfoPage;
