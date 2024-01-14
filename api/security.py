import datetime
import logging
import os

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext

from db import database, user_table

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def access_token_expires() -> int:
    return 30


def create_access_token(email: str):
    logger.info(f"Creating access token for email: {email}")
    expires = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=access_token_expires()
    )
    jwt_data = {"sub": email, "exp": expires}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    logger.info(f"Getting user with email: {email}")
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result


async def authenticate_user(email: str, password: str):
    logger.info(f"Authenticating user with email: {email}")
    user = await get_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return user
