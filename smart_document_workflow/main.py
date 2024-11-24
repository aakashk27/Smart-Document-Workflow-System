from typing import Annotated
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer
from file_upload.app import upload_document
from auth.app import login_user, register_user
from auth.models import Login, Register
from smart_document_workflow.custom_auth import custom_openapi


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.openapi = lambda: custom_openapi(app)

@app.post("/upload/")
async def upload_d(*, file: UploadFile = File(...), token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        response = await upload_document(file,token)
        return response.model_dump()
    except Exception as e:
        return {"error": str(e)}
    

@app.post('/register/')
async def register(user: Register):
    response = await register_user(user)
    return response


@app.post('/login/')
async def login(user: Login):
    response = await login_user(user)
    return response


    
