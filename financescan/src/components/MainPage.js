import React, { useState } from 'react';
import './MainPage.css'; // Import the CSS file

const InfoPage = ({ req_list }) => {
    const [curr_req, setCurrReq] = useState(-1);

    // Function to get the color for an item
    const getItemColor = (key) => {
        return key === curr_req ? 'grey' : 'lightgrey'; // Set color for key '1' to red
    };
    const sortedEntries = Object.entries(req_list).sort(([keyA], [keyB]) => keyB.localeCompare(keyA));


    return (
        <div className="content">
            <div className="requests">
                <div className="scrollable-container">
                    {sortedEntries.map(([key, value], index) => (
                        <div onClick={() => { console.log('hi'); setCurrReq(key); }} className='item'
                            key={key} style={{ backgroundColor: getItemColor(key) }}>{key}: {value["Description"]}, Status: {value["Status"]}, Requested Cost: {value["Requested Cost"]}</div>
                    ))}
                </div>
                <button class="submit_btn">Submit Request</button>
            </div>
            <div class={curr_req !== -1 ? "curr_content" : "disabled"}>
                Requestee: {req_list[curr_req]["Requestee"]}{"\n"}Date: {req_list[curr_req]["Request Date"]}
                {console.log(req_list)}
            </div>
        </div >

    );
};

export default InfoPage;
