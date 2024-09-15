from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google_scan import *
from drive_interface import *
from typing import Dict
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List

app = FastAPI()


f = MasterSheetInterface()
d = DriveInterface()

# Allow CORS for your React frontend
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/auth/{nu_id}")
def read_item(nu_id: str):
    print( nu_id )
    f.authorize(nu_id)
    return f.user

@app.get("/req_list")
def read_item():
    print( 'Fetching req list')
    return f.get_req_list()

@app.get("/options")
def read_item():
    print('Getting options')
    return f.get_request_options()

@app.post("/submit/request")
async def submit_request(request:Dict):
    print( request )
    f.add_request(request)
    return {}

@app.post("/approve")
async def submit_approval(approval:Dict):
    f.add_approval( approval['approved'], approval['request'], approval['id'], approval['user'], approval['note'])
    return

@app.post("/submit/final")
async def submit_final(data:Dict):
    link = d.add_temp_files(data['ID'])
    f.add_final( data['Cost'], data['Tax'], data['Request'], data['ID'], link )
    return

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