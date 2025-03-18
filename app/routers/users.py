from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException

from app.models.User import User
from app.database import users

router = APIRouter(prefix="/api/users")



@router.get("/", status_code=HTTPStatus.OK)
def get_users() -> Iterable[User]:
    return users.get_users()

@router.get("/{user_id}")
async def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user

