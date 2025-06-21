# auths.py

from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    full_name: str
    role: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str
    role: str
