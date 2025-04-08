
from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, HTTPException

from app.models.User import User, UserCreate, UserUpdate
from app.database import users

router = APIRouter(prefix="/api/users")




@router.get("/", status_code=HTTPStatus.OK)
async def get_users() -> Iterable[User]:
    return users.get_users()

@router.get("/{user_id}")
async def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.post("/", status_code=HTTPStatus.CREATED)
async def create_user(user: UserCreate) -> UserCreate:
    try:
        UserCreate.model_validate(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
async def update_user(user_id: int, user: User):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")

    try:
        UserUpdate.model_validate(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))

    updated_user = users.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return updated_user


@router.delete("/delete/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    result = users.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

