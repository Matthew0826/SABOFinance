import logo from './logo.svg';
import './App.css';
import TopBar from './components/TopBar'; // Adjust the path according to your project structure
import SplashPage from './components/SplashPage';
import MainPage from './components/MainPage'
import Request from './components/requests/Request';
import axios from 'axios';
import React, { useState, useEffect } from 'react'; // Ensure this line is correct

function App() {


  const onSignIn = (text) => {
    console.log(text)
  }
  /*
    useEffect(() => {
      axios.get('http://127.0.0.1:8000/auth/002761220')
        .then(response => {
          console.log(response.data);
        });
    }, []);
    */
  return (
    <div className="App">
      <TopBar onSignIn={onSignIn}></TopBar>
      <header className="App-header">
        {false ? <SplashPage></SplashPage> : <MainPage></MainPage>}
      </header>
    </div >
  );
}

export default App;
