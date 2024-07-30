import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_KEY = '46aa319996c9d51bf55cac58c1a3cff9e46d97a2';
const SPREADSHEET_ID = '1JXHfYJCOjfiZ967um8To54fYh7Iol1BYHQOeopLBucI';
const RANGE = 'Students!A1:C10';

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const url = `https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${RANGE}?key=${API_KEY}`;

      try {
        const response = await axios.get(url);
        setData(response.data.values);
      } catch (error) {
        console.error('Error fetching data', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Google Sheets Data</h1>
      <table>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default App;