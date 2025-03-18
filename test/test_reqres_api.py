from http import HTTPStatus

import requests
import pytest


@pytest.mark.parametrize("page", [2])
def test_get_users(page: int, app_url: str) -> None:
    response = requests.get(f"{app_url}/api/users", params={"page": page})
    assert response.status_code == 200
    print(response.url)

@pytest.mark.parametrize("user_id", [2])
def test_get_single_user(user_id: int, app_url: str) -> None:
    response = requests.get(f"{app_url}/api/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["id"] == user_id


