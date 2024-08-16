import logo from './logo.svg';
import './App.css';
import TopBar from './components/TopBar'; // Adjust the path according to your project structure
import SplashPage from './components/SplashPage';
import MainPage from './components/MainPage';
import axios from 'axios';
import React, { useState } from 'react';

function App() {
  const [username, setUsername] = useState('');
  const [req_list, setReqList] = useState({});

  const onSignIn = (text) => {
    const url = `http://127.0.0.1:8000/`;
    axios.get(url + `auth/${text}`)
      .then(response => {
        // Assuming the API response contains a 'username' field
        console.log(response.data)
        setUsername(response.data.Name || ''); // Update the username state
        axios.get(url + 'req_list')
          .then(response => {
            setReqList(response.data)
          })
      })
      .catch(error => {
        console.error('Error fetching data:', error); // Handle errors
      });


  };


  return (
    <div className="App">
      <TopBar onSignIn={onSignIn} username={username} />
      <header className="App-header">
        {username === '' ? <SplashPage /> : <MainPage req_list={req_list} />}
      </header>
    </div>
  );
}

export default App;
