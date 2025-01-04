from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google_scan import *
from drive_interface import *
from typing import Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List
from FinanceInterface import FinanceInterface

""" 
This is the main website that deals with the API routing
This should really only call external functions to handle logic
"""
app = FastAPI()
f = MasterSheetInterface()
d = DriveInterface()
finance_interface = FinanceInterface()

# These are the hosts that can access the backend.
origins = [
    "http://localhost:3000",
    "https://northeasternseds.com",
]

#Middleware that handles the acceptable origins and the heading
app.add_middleware( CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

#This is the root. It gives information on the backend. This will appear when typing api.northeasternseds.com
@app.get("/")
async def read_root():
    return ["Welcome to the Northeastern SEDS finance backend!", 
        "Use the auth/ path to sign in and get an access token!", 
        "Access tokens will expire after 5 minutes with no use",
        "See the documentation on Notion for more info:", 
        "https://www.notion.so/nurover/SEDS-Finance-API-127988be2f3b80d0b68cd89eadc258b8?pvs=4"]

'''
--- AUTHENTIFICATION LOGIC ---
This logic handles how to authenticate and verify a user. There is documentation on this on Notion.
Each user signs in with their NUId and a password. If they do not have a password, the system asks them to create one.
For now, the password will be stored on the Master Finance Sheet (MFS).
'''

# This is the way to authenticate a user
@app.get("/auth")
async def read_item(nuid: str = '', password: str = ''):
    return finance_interface.sign_in(nuid, password)

'''
--- DATA LOGIC ---
This logic handles accessing requests from the frontend
'''

# This gets information about a user
@app.get("/user")
async def read_item(token:str = ''):
    return finance_interface.get_user_info(token)

# This gets all requests visible to the user
@app.get("/requests")
async def read_item(token:str = ''):
    return finance_interface.get_visible_requests(token)

# This gets a specific request
@app.get("/requests/{rqid}")
async def read_item(rqid:str, token:str=''):
    return finance_interface.get_request(int(rqid), token)

#This is the new way to get the data. There are a series of fields.
@app.get("/data")
async def read_item(skip: int = 0, limit: int = 10):
    if( limit == 0 ):
        return HTMLResponse(status_code=401)
    else:
        return skip

@app.get("/req_list")
async def read_item():
    print( 'Fetching req list')
    return f.get_req_list()

@app.get("/options")
async def read_item():
    print('Getting options')
    return f.get_request_options()

@app.post("/submit/request")
async def submit_request(request:Dict):
    print( request )
    f.add_request(request)
    return {}

@app.post("/approve")
async def submit_approval(approval:Dict):
    f.add_approval( approval['approved'], approval['id'], approval['user'], approval['note'])
    return

@app.post("/submit/final")
async def submit_final(data:Dict):
    link = d.add_temp_files(data['ID'])
    f.add_final( data['Cost'], data['Tax'], data['ID'], data['NUId'], link )
    return

#This gets whenever the Excel sheet updates
@app.post("/webhook")
async def receive_webhook(data: Dict):
    print(f"Received data: {data}")
    finance_interface.on_webhook(data['sheetName'])
    return {}

@app.post("/upload/{id}")
async def upload_files(id: str, file_uploads: list[UploadFile]):

    # Create the folder if it doesn't already exist
    if not os.path.exists(f'temp_{id}'):
        os.makedirs(f'temp_{id}')

    for i in range( len( file_uploads ) ):
        data = await file_uploads[i].read()
        with open(f'temp_{id}/'+ file_uploads[i].filename, 'wb') as f:
            f.write(data)
    return
