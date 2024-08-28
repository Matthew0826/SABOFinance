import logo from './logo.svg';
import './App.css';
import TopBar from './components/TopBar'; // Import the TopBar component
import SplashPage from './components/SplashPage'; // Import the SplashPage component
import MainPage from './components/MainPage'; // Import the MainPage component
import axios from 'axios'; // Import axios for making HTTP requests
import React, { useState } from 'react'; // Import React and useState hook

function App() {
  // State to store the username of the signed-in user
  const [username, setUsername] = useState('');
  // State to store the user's details
  const [user, setUser] = useState({});
  // State to store the request list
  const [req_list, setReqList] = useState({});

  const [options, setOptions] = useState({});

  const url = `http://127.0.0.1:8000/`; // Base URL for the API

  // Function to handle sign-in action
  const onSignIn = (text) => {
    // Make a GET request to authenticate the user
    axios.get(url + `auth/${text}`)
      .then(response => {
        // Assuming the API response contains a 'Name' field
        console.log(response.data);
        setUsername(response.data.Name || ''); // Update the username state
        setUser(response.data || {}); // Update the user state
        // Make another GET request to fetch the request list after authentication
        axios.get(url + 'req_list')
          .then(response => {
            getOptions();
            setReqList(response.data); // Update the req_list state with the fetched data
          })
      })
      .catch(error => {
        console.error('Error fetching data:', error); // Handle errors
      });
  };

  const getOptions = () => {
    axios.get(url + `options`)
      .then(response => {
        setOptions(response.data)
      })
  };

  return (
    <div className="App">
      {/* TopBar component with the onSignIn function passed as a prop */}
      <TopBar onSignIn={onSignIn} username={username} />
      <header className="App-header">
        {/* Conditionally render SplashPage or MainPage based on whether the username is set */}
        {username === '' ? <SplashPage /> : <MainPage req_list={req_list} user={user} options={options} />}
      </header>
    </div>
  );
}

export default App;
