from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    return UserSchema(
        username=token + "fakedecoded", email="john@example.com"
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

def fake_hash_password(password: str):
    return password + "_NOTREALLYHASHED"