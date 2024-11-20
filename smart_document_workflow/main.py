from fastapi import FastAPI, File, UploadFile
from file_upload.app import upload_document
from auth.app import login_user, register_user
from auth.models import Login, Register


app = FastAPI()

@app.post("/upload/")
async def upload_d(file: UploadFile = File(...)):
    try:
        response = await upload_document(file)
        return response.model_dump()
    except Exception as e:
        return {"error": str(e)}
    

@app.post('/register/')
async def register(user: Register):
    try:
        response = await register_user(user)
        return response
    except Exception as e:
        return {"error": str(e)}


@app.post('/login/')
async def login(user: Login):
    try:
        response = await login_user(user)
        return response
    except Exception as e:
        return {"error": str(e)}

    
