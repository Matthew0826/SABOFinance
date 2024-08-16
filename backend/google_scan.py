import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import sys

sys.path.append('..')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\geisel.m\Documents\Clubs\SEDS\SABOFinance\backend\secret_key.json")
AUTH_END_INDEX = "G"
SHEET_NAMES = ["Students", "Requests"]

#sheet.update_cell(2, 3, "test")
#The interface with the Master Finance Sheet
class MasterSheetInterface():

    #Default initialization 
    def __init__( self ):
        self.drive = gspread.authorize(CREDENTIALS)
        self.file = self.drive.open("SEDS Master Finance Sheet 2024-2025")

        self.sheet_data = {}
        for sheet in SHEET_NAMES:
            self.sheet_data[sheet] = self.file.worksheet(sheet).get_all_values()
        
        self.user = {}

    #This refreshes the webpage
    def refresh(self, pagename):
        self.sheet_data[pagename] = self.file.worksheet(pagename).get_all_values()

    #Authorize the user based on NuID
    def authorize( self, nuID ):
        print(nuID)
        self.user = {}
        try:
            self.refresh("Students")
            for i in range(1, len(self.sheet_data["Students"])):
                #Check if the element is the correct user
                if( self.sheet_data["Students"][i][0] == nuID ):
                    for j in range(len(self.sheet_data["Students"][0])):
                        self.user[self.sheet_data["Students"][0][j]] = self.sheet_data["Students"][i][j]
        except:
            self.user = {}
        
    #This gets the request list
    def get_req_list( self ):
        if self.user == {}:
            return {}
        
        requests = {}

        self.refresh("Requests")

        for i in range(1, len(self.sheet_data["Requests"])):
            curr_element = {}
            for j in range(1, len(self.sheet_data["Requests"][0])):
                curr_element[self.sheet_data["Requests"][0][j]] = self.sheet_data["Requests"][i][j]
            requests[int(self.sheet_data["Requests"][i][0])] = curr_element
        print( requests )
        return requests
    #This gets ths user's requests
    def getUserRequests(self):
        self.refresh("Purchases")
        
if __name__ == '__main__':
    f = MasterSheetInterface()
    f.authorize("002761220")
    f.get_req_list()
    #print( f.user )