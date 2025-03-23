import json
import os
from http import HTTPStatus

import dotenv
import pytest
import requests
from faker import Faker

faker = Faker()

@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("BASE_URL")


@pytest.fixture(scope="module")
def fill_test_data(app_url: str):
    with open("../qaguru-advanced-playground/users.json") as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        assert response.status_code == HTTPStatus.CREATED
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        response = requests.delete(f"{app_url}/api/users/delete/{user_id}")
        assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.fixture
def users(app_url: str):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture
def user_data() -> dict[str, str]:
    email = faker.email(domain="ramdom.data")
    first_name = faker.first_name()
    last_name = faker.last_name()
    avatar = f"https://reqres.in/img/faces/{first_name}-{last_name}.jpg"

    user_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "avatar": avatar
    }

    return user_data


@pytest.fixture
def clear_generated_user(app_url: str):
    """Фикстура для удаления созданного пользователя после теста."""
    user_ids = []
    yield user_ids

    for user_id in user_ids:
        response = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NO_CONTENT




