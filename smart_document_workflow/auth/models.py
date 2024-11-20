from pydantic import BaseModel


class Register(BaseModel):
    username: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class token(BaseModel):
    access_token: str
    token_type: str