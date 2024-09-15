from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

class DriveInterface:
    def __init__(self):
        # Path to your service account credentials file
        SERVICE_ACCOUNT_FILE = 'secret_key.json'

        # Define the required scopes for Google Drive
        SCOPES = ['https://www.googleapis.com/auth/drive.file']

        # Authenticate using the service account
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Build the Google Drive API client
        self.service = build('drive', 'v3', credentials=credentials)


    def create_folder(self, folder_name, parent_id=None):
        # Metadata for the new folder
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id] if parent_id else []
        }
        
        # Create the folder
        folder = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()
        
        print(f'Folder "{folder_name}" ID: {folder.get("id")}')
        return folder.get('id')


    def upload_file_to_drive(self, file_path, file_name, folder_id):
        # File metadata for Google Drive
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]  # Place the file in the specified folder
        }

        # Media content to upload
        media = MediaFileUpload(file_path, resumable=True)

        # Upload the file to Google Drive
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        file_id = file.get('id')
        print(f'File ID: {file_id}')

        # Make the file publicly accessible and get the shareable link
        drive_file = self.service.files().get(fileId=file_id, fields='webViewLink').execute()
        file_link = drive_file.get('webViewLink')
        print(f'File Link: {file_link}')

        return file_link
    
    def add_temp_files(self, id):
        parent_folder_id = '1IVeLYbmaRRNqD2Uys6DDRz_Fkb7elRnY'  # Replace with your folder ID
        folder_id = self.create_folder('request_' + id, parent_folder_id)

        file_id = 0
        
        for root, dirs, files in os.walk(r"C:\Users\geisel.m\Documents\Clubs\SEDS\SABOFinance\backend\temp_" + id):
                    for name in files:
                        self.upload_file_to_drive( root + "\\" + name, 'reciept_' + str(file_id), folder_id ) 
                        file_id += 1

        return f"https://drive.google.com/drive/folders/{folder_id}"

# Define the parent folder ID where you want to create the new subfolder

# Create a new subfolder named "subfolder" inside the specified folder
#ubfolder_id = create_folder('subfolder', parent_id=parent_folder_id)

# Upload a file to the newly created subfolder and get its link
#file_link = upload_file_to_drive(r'APP33600.pdf', 'uploaded_file.txt', subfolder_id)
