import React, { useState } from 'react';
import './Request.css'; // Import the CSS file

const Request = (request) => {
    return (
        <div class="main">
            <img class="project-src" src="rover.png"></img>
            <div class="description">
                <p>I want a puppy</p>
                <p>Requestee: Matthew Geisel Status: </p>
            </div>
        </div>
    );
};

export default Request;
