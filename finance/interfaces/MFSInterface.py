'''
This class deals with interacting with the Master Finance Sheet (MFS).
It handles base-level reading, writing, and querying.
Try to make this as dynamic as possible.
'''
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import shutil
import sys
from typing import List, Tuple

# Add the parent directory to the system path for imports
sys.path.append('..')

class MFSInterface:
    
    ''' Default initialization of the sheet. Signs in & gets info '''
    def __init__(self):
        # The name of the file we are opening
        FILENAME = "SEDS Master Finance Sheet 2024-2025"

        # Load the credentials from the JSON key file for the API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(r"secret_key.json")

        # Authorize & initialize the Google Sheets client
        self._sheets = gspread.authorize(credentials)
        # Open the Master Finance Sheet
        self._file = self._sheets.open(FILENAME)

    ''' HELPER FUNCTIONS '''
    # This gets & processes the data from a sheet
    def _get_sheet_data(self, sheet_name:str):
        # Check if the sheet name is in memory
        raw_sheet_data = self._file.worksheet(sheet_name).get_all_values()
            
        # Now process the list
        formatted_sheet_data = {}
        for i in range(len(raw_sheet_data[0])):
            if raw_sheet_data[0][i] == '':
                continue
            else:
                formatted_sheet_data[raw_sheet_data[0][i].lower().replace(' ', '_')] = [row[i] for row in raw_sheet_data[1:]]
        
        #Return the processed data
        return formatted_sheet_data

    # Write to a cell based on its header and a specific variable
    # Row is a tuple of the variable name and value
    def _write_to_cell(self, sheet_name:str, variable_name:str, search_variable:Tuple[str, str], data:str ):
        # Get the sheet's data
        sheet_data = self._get_sheet_data(sheet_name)

        # Find the index of the row
        row_index = sheet_data[search_variable[0]].index(search_variable[1]) + 2

        # Find the index of the column
        column_index = list(sheet_data.keys()).index(variable_name) + 1
        column_letter = chr(column_index + 64)             # Convert to a capital letter
        
        # Write the data
        self._file.worksheet(sheet_name).update([[data]], column_letter + str(row_index))
        

    # This function resolves permissions issues
    @staticmethod
    def has_viewing_permission(project_name:str, subteam_name:str, permissions:List[str]) -> bool:
        # Finance members have all viewing permissions
        if 'Finance' in permissions:
            return True
        # Admins have viewing permissions for all purchases of their project
        elif project_name + ' Admin' in permissions:
            return True
        # Leads have viewing permissions for all purchases of their subteam
        elif '(' + project_name + ') ' + subteam_name + ' Lead' in permissions:
            return True
        return False
    
    # This updates the sheet name
    def update(self, sheet_name:str):
        self._sheet_data[sheet_name] = self._file.worksheet(sheet_name).get_all_values()

    ''' MFS ACCESSOR FUNCTIONS '''
    def get_request_options(self):
        # Get the data and format it
        raw_dict = self._get_sheet_data("Request Options")
        for key in raw_dict:
            raw_dict[key] = [item for item in raw_dict[key] if item != '']
        return raw_dict


    ''' Get the info for a specific student '''
    def get_student_info(self, nuid:str):
        # Get the data from the student sheet
        student_data = self._get_sheet_data("Students")
        
        # Get the index of the selected student
        student_index = student_data['nuid'].index(str(nuid))
        
        # Return the dictionary
        return dict(zip(student_data.keys(), [value[student_index] for value in student_data.values()]))
    
    ''' Get the info for all students '''
    def get_all_students(self):
        # Get the data from the student sheet
        student_data = self._get_sheet_data("Students")

        student_dict = {}
        for i in range(len(student_data['name'])):
            student_dict[student_data['name'][i]] = dict(zip(student_data.keys(), [value[i] for value in student_data.values()]))
        return student_dict

    ''' Get the info for a specific request '''
    def get_request_info(self, request_id:int):
        # Get the data from the request sheet
        request_data = self._get_sheet_data("Requests")
        
        #Get the index of the selected id
        request_index = request_data['id'].index(str(request_id))

        #Return the parsed dictionary
        return dict(zip(request_data.keys(), [value[request_index] for value in request_data.values()]))

    ''' Get all requests that can be viewed given a name and permission list '''
    def get_requests_by_permissions(self, nuid:str, permissions:List[str]):
        # Get the data from the request sheet
        request_data = self._get_sheet_data(sheet_name="Requests")
        
        # Get the name of the user from nuid
        student_data = self._get_sheet_data(sheet_name="Students")
        name = student_data['name'][student_data['nuid'].index(str(nuid))]
    
        # Go through each element and check if we have permissions to view it. If so, add it
        all_requests = {}
        for i in range(len(request_data['id'])):
            if request_data['requestee'][i] == name or MFSInterface.has_viewing_permission(request_data['project_name'][i], request_data['subteam_name'][i], permissions):
                all_requests[request_data['id'][i]] = dict(zip(request_data.keys(),[row[i] for row in request_data.values()]))
        return all_requests

    ''' This gets all of the requests '''
    def get_all_requests(self):
        # Get the data from the student sheet
        request_data = self._get_sheet_data("Requests")
    
        # Go through and process into a correctly formatted dictionary
        request_dict = {}
        for i in range(len(request_data['id'])):
            request_dict[request_data['id'][i]] = dict(zip(request_data.keys(), [value[i] for value in request_data.values()]))
        return request_dict

    ''' Get the permissions for a given user '''
    def get_permissions(self, nuid:str):
        # Get the student data
        student_data = self._get_sheet_data("Students")

        # Get the correct student
        student_index = student_data['nuid'].index(nuid)
        permission_string = student_data['permissions'][student_index]

        # Parse the permission string
        return [value.strip() for value in permission_string.split('/')]
    
    ''' Get the hashed password for a given user '''
    def get_hashed_password(self, nuid:str):
        # Get the student data
        student_data = self._get_sheet_data("Students")

        # Get the correct student
        student_index = student_data['nuid'].index(nuid)
        return student_data['hashed_password'][student_index]

    ''' MUTATORS '''
    
    ''' Write the hashed password for a given password '''
    def set_hashed_password(self, nuid:str, hashed_password:str):
        self._write_to_cell('Students', 'hashed_password', ('nuid', nuid), hashed_password)

if __name__ == '__main__':
    mfsInterface = MFSInterface()
    print( 'initialized!' )
    mfsInterface.set_hashed_password('002761220', 'test')
    print(mfsInterface.get_hashed_password('002761220'))

