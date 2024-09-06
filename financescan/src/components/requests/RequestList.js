import React from 'react';
import './RequestList.css';

const RequestList = ({ req_list, setCurrReq, currReq }) => {
    // Sort the requests list by key in descending order for display
    const sortedEntries = Object.entries(req_list).sort(([keyA], [keyB]) => keyB.localeCompare(keyA));

    // Function to set background color based on selected request
    const getItemColor = (key) => {
        return key === currReq ? 'grey' : 'lightgrey';
    };

    return (
        <div className="scrollable-container">
            {/* Render each sorted request with its description and cost */}
            {sortedEntries.map(([key, value]) => (
                <div
                    onClick={() => setCurrReq(key)} // Set the selected request key when clicked
                    className='item'
                    key={key}
                    style={{ backgroundColor: getItemColor(key) }}
                >
                    {/* Display request details */}
                    {value["Requestee"]} requested {value["Description"]}<br />
                    Requested Cost: ${value["Requested Cost"]}
                </div>
            ))}
        </div>
    );
};

export default RequestList;
