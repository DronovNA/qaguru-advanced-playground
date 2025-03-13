from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi_pagination import paginate, Page

from app.models.AppStatus import AppStatus
from app.models.user import User
from app.utils import load_users

router = APIRouter()
users = load_users()


@router.get("/status", status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    return AppStatus(status="ok")

@router.get("/api/users/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    return paginate(users)

@router.get("/api/users/{user_id}")
async def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]

