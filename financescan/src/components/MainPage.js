import React, { useState, useEffect } from 'react'; // Import necessary React hooks
import './MainPage.css'; // Import the CSS file for styling
import RequestList from './requests/RequestList';
import Request from './requests/Request';
import NewRequest from './requests/NewRequest';
import ApprovedRequest from './requests/ApprovedRequest';

const MainPage = ({ req_list, user, options, postRequest, postApproval, postFiles }) => {

    // State to track the selected request (default: -1 meaning none selected)
    const [curr_req, setCurrReq] = useState(-1);


    // Sort the requests list by key in descending order for display
    const sortedEntries = Object.entries(req_list).sort(([keyA], [keyB]) => keyB.localeCompare(keyA));


    return (
        <div className="content">
            {/* Section for displaying requests */}
            <div className="requests">
                <RequestList req_list={req_list} setCurrReq={setCurrReq} currReq={curr_req}></RequestList>
                <button class="submit_btn" onClick={() => setCurrReq(-2)}>Add Request</button>
            </div>

            {/* Conditional rendering of the selected request content */}
            <div className={curr_req >= 0 ? "curr_content" : "disabled"}>
                <Request curr_req={curr_req} sortedEntries={sortedEntries} req_list={req_list} user={user} postApproval={postApproval}></Request>
                <ApprovedRequest curr_req={curr_req} sortedEntries={sortedEntries} req_list={req_list} user={user} postApproval={postApproval} postFiles={postFiles}></ApprovedRequest>
            </div>

            {/* If the 'Add Request' button is clicked, display the submission form */}
            <NewRequest curr_req={curr_req} setCurrReq={setCurrReq} options={options} user={user} postRequest={postRequest}></NewRequest>
        </div>
    );
};

export default MainPage;
