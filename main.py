from fastapi import FastAPI, Request, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google_scan import *
from drive_interface import *
from typing import Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List
from FinanceInterface import FinanceInterface
import json

""" 
This is the main website that deals with the API routing
This should really only call external functions to handle logic
"""
app = FastAPI()
# f = MasterSheetInterface()
# d = DriveInterface()
finance_interface = FinanceInterface()

# These are the hosts that can access the backend.
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
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

@app.post("/request")
async def submit_request(
    token: str = Query(..., description="Authentication token as a query parameter"),
    request: Dict = Body(..., description="Request body containing the data"),):    
    finance_interface.add_request(token, request)
    return {}

@app.post("/requests/{rqid}/approval")
async def submit_request(rqid:str, token:str = Query(), request:Dict = Body()):
    print( request )
    finance_interface.add_approval(token, rqid, approval=request)

# This gets the options for requests
@app.get("/options")
async def read_item():
    return finance_interface.get_options()

# This gets a specific request
@app.get("/requests/{rqid}")
async def read_item(rqid:str, token:str=''):
    return finance_interface.get_request(int(rqid), token)

#This gets whenever the Excel sheet updates
@app.post("/webhook")
async def receive_webhook(data: Dict):
    print(f"Received data: {data}")
    finance_interface.on_webhook(data['sheetName'])
    return {}

@app.post("/request/{rqid}/upload")
async def upload_files(
    rqid: str, 
    token: str = Query(...),  # Required query parameter
    data: str = Body(...),  # JSON body
    file_uploads: List[UploadFile] = File(...)  # List of files
):
    data = json.loads(data)
    rqid = data['rqid']
    print(data)
    # Create the folder if it doesn't already exist
    if not os.path.exists(f'temp/temp_{rqid}'):
        os.makedirs(f'temp/temp_{rqid}')

    for i in range( len( file_uploads ) ):
        data = await file_uploads[i].read()
        with open(f'temp/temp_{rqid}/'+ file_uploads[i].filename, 'wb') as f:
            f.write(data)
    return

