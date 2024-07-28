// client/src/components/SpreadsheetData.js
import React, { useState, useEffect } from 'react';
import { gapi } from 'gapi-script';
import { initClient } from '../utils/gapi';

const SPREADSHEET_ID = '1qbCcjiO8y9Fz0yAJm2HxnzlmC02w3zv5xGx1-TpaFHs';
const RANGE = 'BTS';

function SpreadsheetData() {
    const [data, setData] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        initClient();
    }, []);

    const handleAuthClick = () => {
        gapi.auth2.getAuthInstance().signIn().then(() => {
            setIsAuthenticated(true);
            fetchData();
        });
    };

    const handleSignOut = () => {
        gapi.auth2.getAuthInstance().signOut().then(() => {
            setIsAuthenticated(false);
            setData(null);
        });
    };

    const fetchData = () => {
        gapi.client.sheets.spreadsheets.values.get({
            spreadsheetId: SPREADSHEET_ID,
            range: RANGE,
        }).then(response => {
            setData(response.result.values);
        }).catch(error => {
            console.error('Error fetching data', error);
        });
    };

    const updateData = () => {
        gapi.client.sheets.spreadsheets.values.update({
            spreadsheetId: SPREADSHEET_ID,
            range: 'BTS!C2',
            valueInputOption: 'USER_ENTERED',
            resource: {
                values: [["2. Sophomore"]],
            },
        }).then(response => {
            console.log('Data updated', response);
        }).catch(error => {
            console.error('Error updating data', error);
        });
    };

    return (
        <div>
            <h1>Spreadsheet Data</h1>
            {!isAuthenticated ? (
                <button onClick={handleAuthClick}>Sign in with Google</button>
            ) : (
                <>
                    <button onClick={handleSignOut}>Sign out</button>
                    <button onClick={fetchData}>Fetch Data</button>
                    <button onClick={updateData}>Update Data</button>
                    {data ? (
                        <pre>{JSON.stringify(data, null, 2)}</pre>
                    ) : (
                        <p>Loading data...</p>
                    )}
                </>
            )}
        </div>
    );
}

export default SpreadsheetData;
