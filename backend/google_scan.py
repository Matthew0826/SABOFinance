import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import sys
from datetime import datetime

# Add the parent directory to the system path for module imports
sys.path.append('..')

# Define the scope for Google Sheets API access
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# Load credentials from the JSON key file for Google Sheets API
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\geisel.m\Documents\Clubs\SEDS\SABOFinance\backend\secret_key.json")
AUTH_END_INDEX = "G"
# Define the sheet names that will be accessed
SHEET_NAMES = ["Students", "Requests", "Request Options"]

# Commented out sample code to update a cell in a sheet
# sheet.update_cell(2, 3, "test")

# The interface with the Master Finance Sheet
class MasterSheetInterface:

    # Default initialization
    def __init__(self):
        # Authorize and initialize the Google Sheets client
        self.drive = gspread.authorize(CREDENTIALS)
        # Open the specific Google Sheet by name
        self.file = self.drive.open("SEDS Master Finance Sheet 2024-2025")

        # Initialize a dictionary to store sheet data
        self.sheet_data = {}
        for sheet in SHEET_NAMES:
            # Retrieve all values from each sheet and store them in the dictionary
            self.sheet_data[sheet] = self.file.worksheet(sheet).get_all_values()
        
        # Initialize an empty user dictionary
        self.user = {}

    # Refreshes the data of a specified sheet
    def refresh(self, pagename):
        # Update the local copy of the sheet data
        self.sheet_data[pagename] = self.file.worksheet(pagename).get_all_values()

    # Authorize the user based on NuID
    def authorize(self, nuID):
        print(nuID)
        # Reset user information
        self.user = {}
        try:
            # Refresh the data from the "Students" sheet
            self.refresh("Students")
            # Loop through the rows in the "Students" sheet
            for i in range(1, len(self.sheet_data["Students"])):
                # Check if the current row matches the provided NuID
                if self.sheet_data["Students"][i][0] == nuID:
                    # Populate the user dictionary with the student's information
                    for j in range(len(self.sheet_data["Students"][0])):
                        self.user[self.sheet_data["Students"][0][j]] = self.sheet_data["Students"][i][j]
        except:
            # If an error occurs, reset the user information
            self.user = {}
        
    # Retrieves the request list from the "Requests" sheet
    def get_req_list(self):
        # If no user is authorized, return an empty dictionary
        if self.user == {}:
            return {}
        
        # Initialize an empty dictionary for requests
        requests = {}

        # Refresh the data from the "Requests" sheet
        self.refresh("Requests")

        # Loop through the rows in the "Requests" sheet
        for i in range(1, len(self.sheet_data["Requests"])):
            # Initialize a dictionary to store the current request's data
            curr_element = {}
            for j in range(1, len(self.sheet_data["Requests"][0])):
                # Populate the current request dictionary with data from the sheet
                curr_element[self.sheet_data["Requests"][0][j]] = self.sheet_data["Requests"][i][j]
            # Add the current request to the requests dictionary using its ID as the key
            requests[int(self.sheet_data["Requests"][i][0])] = curr_element
        
        print(requests)
        return requests
    
    # Placeholder method to get the user's requests (not yet implemented)
    def getUserRequests(self):
        # Refresh the data from the "Purchases" sheet
        self.refresh("Purchases")
        
    #Gets the options for creating a new request
    def get_request_options(self):
        self.refresh("Request Options")
        return_val = {}
        for i in range(len(self.sheet_data["Request Options"][0])):
            return_val[self.sheet_data["Request Options"][0][i]] = []
            for j in range(1, len(self.sheet_data["Request Options"])):
                if(self.sheet_data["Request Options"][j][i] == ""):
                    continue
                return_val[self.sheet_data["Request Options"][0][i]].append(self.sheet_data["Request Options"][j][i])
        return return_val
    
    def add_request(self, request):
        self.refresh("Requests")
        next_row = len(self.sheet_data["Requests"])             #This is the next row
        try:
            id = max( [float(value) for value in [sub_array[0] for sub_array in self.sheet_data["Requests"][1:] ] if value]) + 1
        except:
            id = 0
        data = [str(int(id)), request["Requestee"], request["Index"], request["Account"], request["Description"], "Pending Approval",
            request["Project"], request["Subteam"], request["Cost"], request["Link"], datetime.now().strftime(str("%m/%d/%Y %H:%M:%S"))]
        print( next_row, data)
        self.file.worksheet("Requests").append_row(data )
    
    APPROVAL_COLS = {"Approver": "L", "Approval Date": "M" }
    ADMIN_COLS = {"Admin Approver": "O", "Admin Date": "P"}

    def add_approval(self, approval_status, request, id, user, note="" ):
        #Get the current ID
        id = int(id) + 2
        print( 'adding approval')
        #Refresh the relevant data
        self.refresh("Request Options")

        #See if this is a minor purchase
        minor_purchase = request["Requested Cost"] < self.sheet_data["Request Options"][1][5]

        #Check if the user is an admin
        is_admin = 'Admin' in user['Permissions'] and request['Project'] in user['Permissions']

        if( approval_status ):
            status = "Approved" if (minor_purchase or is_admin) else "Pending Admin Approval"
        else:
            status = "Admin Denied" if is_admin else "Denied"

        #Check if it is an admin user issuing permissions
        if( 'Admin' in user['Permissions'] and request['Project'] in user['Permissions'] and request['Status'] == "Pending Admin Approval" ):
            range = self.ADMIN_COLS["Admin Approver"] + str(id) + ":" + self.ADMIN_COLS["Approval Date"] + str(id)
            self.file.worksheet("Requests").update( range, [[user["Name"], datetime.now().strftime(str("%m/%d/%Y %H:%M:%S"))]])
            self.file.worksheet("Requests").update( f"F{id}", [[status]])


        #Check if it is a business 
        elif('Business' in user['Permissions'] and request['Status'] == "Pending Approval"):
            range = self.APPROVAL_COLS["Approver"] + str(id) + ":" + self.APPROVAL_COLS["Approval Date"] + str(id)
            self.file.worksheet("Requests").update( range, [[user["Name"], datetime.now().strftime(str("%m/%d/%Y %H:%M:%S"))]])
            self.file.worksheet("Requests").update( f"F{id}", [[status]])
                
        
        if( note != "" ):
            self.file.worksheet("Requests").update( f"V{id}", [[note]])
        
        

if __name__ == '__main__':
    # Create an instance of the MasterSheetInterface class
    f = MasterSheetInterface()
    # Authorize a user using their NuID
    f.authorize("002761220")
    # Retrieve the request list
    f.get_req_list()

    # print(f.user)  # Uncomment to print the authorized user's data
