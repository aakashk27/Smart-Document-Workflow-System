

from fastapi import HTTPException
from auth.services import create_access_token, get_password_hash, verify_password
from file_upload.app import db
from auth.models import Login, Register


user_collection = db.user

async def register_user(user: Register):
    if user_collection.find_one({'email': 'user.email'}):
        raise HTTPException(status_code=400, detail='User already exists')
    hashed_pass = get_password_hash(user.password)
    new_user = {'email': user.email, 'username': user.username, 'password': hashed_pass}
    user_collection.insert_one(new_user)
    return {'message': 'User registered successfully'}


async def login_user(user: Login):
    user_data  = user_collection.find_one({'email': user.email})
    if not user_data:
        raise HTTPException(status_code=400, detail='Invalid credentials')
    if not user_data['password'] or not verify_password(user.password, user_data['password']):
        raise HTTPException(status_code=400, detail='Invalid credentials')
    acess_token = create_access_token(data = {'sub': user.email})
    return {'access_token': acess_token, 'token_type': 'bearer'}

    