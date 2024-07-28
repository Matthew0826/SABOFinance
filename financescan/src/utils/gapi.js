// client/src/utils/gapi.js
import { gapi } from 'gapi-script';

const CLIENT_ID = '511555850333-grv85sla1e54rcdmj3fv85hidi24fo57.apps.googleusercontent.com';
const API_KEY = '46aa319996c9d51bf55cac58c1a3cff9e46d97a2';
const DISCOVERY_DOCS = ["https://sheets.googleapis.com/$discovery/rest?version=v4"];
const SCOPES = "https://www.googleapis.com/auth/spreadsheets.readonly https://www.googleapis.com/auth/spreadsheets";

export const initClient = () => {
    gapi.load('client:auth2', () => {
        gapi.client.init({
            apiKey: API_KEY,
            clientId: CLIENT_ID,
            discoveryDocs: DISCOVERY_DOCS,
            scope: SCOPES
        }).then(() => {
            console.log('GAPI client loaded for API');
        }).catch(error => {
            console.error('Error loading GAPI client for API', error);
        });
    });
};
