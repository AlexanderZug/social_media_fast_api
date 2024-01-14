import logging

from fastapi import APIRouter, HTTPException, status

from db import user_table, database
from models.user import UserIn
from security import get_user, get_password_hash, authenticate_user, create_access_token

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)
    logger.info(query)

    await database.execute(query)
    return {"message": "User created"}


@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = await create_access_token(user["email"])
    return {"access_token": access_token, "token_type": "bearer"}
