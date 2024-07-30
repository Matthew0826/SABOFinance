import React, { useState } from 'react';
import './TopBar.css'; // Import the CSS file

const TopBar = ({ onSignIn }) => {
    const [text, setText] = useState('')

    const handleClick = () => {
        onSignIn(text)
    }
    return (
        <div className="top-bar">
            <img class="logo" src="sedslogo.png"></img>
            <div className="nav-links">
                <img src="usericon.png"></img>
                <p>NuID:</p>
                <input class="test" value={text} type="tel" onChange={(event) => setText(event.target.value)} maxLength={9}></input>
                <button onClick={handleClick}>Sign In</button>
            </div>
        </div>
    );
};

export default TopBar;
