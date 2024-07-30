import React, { useState } from 'react';
import './MainPage.css'; // Import the CSS file

const InfoPage = () => {
    return (
        <div className="content">
            <div className="scrollable-container">
                {Array.from({ length: 50 }, (_, i) => (
                    <div className="item" key={i}>Item {i + 1}</div>
                ))}
            </div>
            <button>Submit Request</button>
        </div>

    );
};

export default InfoPage;
