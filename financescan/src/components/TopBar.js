import React, { useState } from 'react';
import './TopBar.css'; // Import the CSS file

const TopBar = ({ onSignIn, username }) => {
    const [text, setText] = useState('')

    const handleClick = () => {
        onSignIn(text)
    }
    return (
        <div className="top-bar">
            <img className="logo" src="sedslogo.png"></img>
            <div className="nav-links">
                <img src="usericon.png"></img>
                <p>{username}</p>
                <p>NuID:</p>
                <input className="test" value={text} type="tel" onChange={(event) => setText(event.target.value)} maxLength={9}></input>
                <button onClick={handleClick}>Sign In</button>
            </div>
        </div>
    );
};

export default TopBar;
