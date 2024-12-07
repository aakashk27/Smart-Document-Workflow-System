from typing import Annotated
from fastapi import Body, Depends, FastAPI, File, UploadFile
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from file_upload.app import upload_document
from auth.app import login_user, register_user
from auth.models import Login, Register
from custom_auth import custom_openapi


app = FastAPI()

@app.post("/upload/")
async def upload_d(
    text: Annotated[str | None, Body(description="Task to do with document")] = "",
    file: UploadFile = File(...),
):  
    return await upload_document(file=file, text=text)


@app.post('/register/')
async def register(user: Register):
    response = await register_user(user)
    return response


@app.post('/login/')
async def login(user: Login):
    response = await login_user(user)
    return response


    
