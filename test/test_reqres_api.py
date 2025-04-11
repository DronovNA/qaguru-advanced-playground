import random
from http import HTTPStatus

import requests
import pytest

from app.models.User import User
from utils.fast_api_app import FastApiApp


@pytest.fixture(scope='function')
def app(env: str):
    return FastApiApp(env)

@pytest.mark.usefixtures("fill_test_data")
def test_users(app: FastApiApp):
    response = app.get_all_users()
    assert response.status_code == HTTPStatus.OK

    user_list = response.json()
    for user in user_list:
        User.model_validate(user)

def test_create_single_user(app: FastApiApp, user_data: dict[str, str], clear_generated_user):
    """Тест на создание пользователя с автоматическим удалением."""
    response = app.create_user(user_data)
    assert response.status_code == HTTPStatus.CREATED
    user: dict = response.json()
    User.model_validate(user)
    del user['id']
    assert user_data == user

    user_id = response.json()["id"]
    clear_generated_user.append(user_id)

@pytest.mark.parametrize("request_data", [
        {
            "email": "testpatch.mail.1@qaguru.autotest",
        },
        {
            "first_name": "TestPatchName1"
        },
        {
            "last_name": "TestPatchLastName1"
        },
        {
            "avatar": "https://reqres.in/img/faces/testpatch-avatar-1.jpg"
        }
])
def test_patch_single_user(app: FastApiApp, fill_test_data, users: list[User], request_data: dict[str]):
    """Тест на изменение с предусловием: наличие созданного пользователя"""
    user: dict = random.choice(users)
    response = app.update_user(user["id"], request_data)
    assert response.status_code == HTTPStatus.OK
    updated_user: dict = response.json()
    User.model_validate(updated_user)
    assert user['id'] == updated_user['id']
    for key in request_data.keys():
        assert user[key] != updated_user[key]

def test_get_user_after_patch(app: FastApiApp, user_data: dict[str, str], fill_test_data, users: list[User]):
    """Тест на Get после изменения"""
    user_patch_data = user_data

    user: dict = random.choice(users)
    response = app.update_user(user["id"], user_data)
    assert response.status_code == HTTPStatus.OK
    updated_user: dict = response.json()
    user_id = updated_user.pop("id", None)
    assert updated_user == user_patch_data

    response = app.get_user_by_id(user_id)
    assert response.status_code == HTTPStatus.OK
    get_user: dict = response.json()
    get_user_id = get_user.pop("id", None)
    assert user_id == get_user_id
    assert get_user == updated_user

@pytest.mark.parametrize("request_data", [
        {
            "method": "post",
            "endpoint": "/api/users/delete/"
        },
        {
            "method": "options",
            "endpoint": "/api/users/"
        }
    ])
def test_users_method_not_allowed(app: FastApiApp, request_data: dict):
    """
    Тест на 405 ошибку. Предусловия: ничего не нужно
    """

    response = app.session.request(method=request_data["method"], url=request_data["endpoint"])
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.parametrize("request_data", [
    {
        "method": "PATCH",
        "json": {
            "email": "1.mail.10@qaguru.autotest"
        }
    }
])
def test_users_method_not_found_patch(app: FastApiApp, fill_test_data, users: list[User], request_data: dict):
    """
    Тест на 404 ошибку при обновлении
    """
    user_ids = [user["id"] for user in users]
    non_existent_user_id = max(user_ids) + 100
    response = app.session.request(
        method=request_data["method"],
        url=f"/api/users/{non_existent_user_id}",
        json=request_data["json"]
    )
    assert response.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.parametrize("request_data", [
    {
        "method": "DELETE",
        "json": None
    }
])
def test_users_method_not_found_delete(app: FastApiApp, fill_test_data, users: list[User], request_data: dict):
    """
    Тест на 404 ошибку при удалении
    """
    user_ids = [user["id"] for user in users]
    non_existent_user_id = max(user_ids) + 10000
    response = app.session.request(
        method=request_data["method"],
        url=f"/api/users/delete/{non_existent_user_id}",
        json=request_data["json"]
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_single_user(app: FastApiApp, fill_test_data, users: list[User]):
    """
    Тест на удаление с предусловием: наличие созданного пользователя
    """
    user: dict = random.choice(users)
    response = app.session.delete(f"/api/users/delete/{user['id']}")
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = app.get_user_by_id(user["id"])
    assert response.status_code == HTTPStatus.NOT_FOUND






