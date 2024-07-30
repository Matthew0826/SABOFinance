import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = ServiceAccountCredentials.from_json_keyfile_name("secret_key.json")

file = gspread.authorize(creds)
workbook = file.open("SEDS Master Finance Sheet 2024-2025")
sheet = workbook.worksheet("Students")

#sheet.update_cell(2, 3, "test")

#User Authorization
def authorize_user(nuId):
    i = 1
    auth_elements = sheet.range("A1:A100")            #Assume a maximum of 100 users

    for element in auth_elements:
        if element.value == '':
            break
        if element.value == nuId:
            auth_details = []
            for element in sheet.range( f"A{i}:G{i}"):
                auth_details.append( element.value )
            return auth_details 
        i += 1
    return element

if __name__ == '__main__':
    print(authorize_user('002761220'))