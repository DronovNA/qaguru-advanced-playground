from http import HTTPStatus

from fastapi import APIRouter

from app.database.engine import check_availability
from app.models.AppStatus import AppStatus

router = APIRouter()

@router.get("/status", status_code=HTTPStatus.OK)
def get_status() -> AppStatus:
    return AppStatus(database=check_availability())