from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
import jwt
from dotenv import dotenv_values
from models import *
from fastapi import status, FastAPI, Depends, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
config_credentials = dict(dotenv_values(".env"))


# Return hashed password
def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if user and verify_password(password, user.password):
        return user
    return False


# Generate JWT token
async def token_generator(username: str, password: str):
    user = await authenticate_user(username, password)
    #
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token or expired token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    #
    token_data = {
        'id': user.id,
        'username': user.username
    }
    #
    token = jwt.encode(token_data, config_credentials['SECRET_KEY'])
    return token


# Verify JWT token
async def verify_token(token: str):
    try:
        payload = jwt.decode(token, config_credentials["SECRET_KEY"], algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user

