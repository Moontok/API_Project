import logging

from fastapi import APIRouter, HTTPException
from socialapi.models.user import UserIn
from socialapi.security import get_user, get_password_hash, authenticate_user, create_access_token
from socialapi.database import database, user_table


router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created"}


@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}