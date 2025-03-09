import requests
import pytest

BASE_URL = "http://127.0.0.1:8000/api"

@pytest.mark.parametrize("page", [2])
def test_get_users(page):
    response = requests.get(f"{BASE_URL}/users", params={"page": page})
    assert response.status_code == 200
    assert "data" in response.json()

@pytest.mark.parametrize("user_id", [2])
def test_get_single_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

@pytest.mark.parametrize("user", [{"name": "morpheus", "job": "leader"}])
def test_create_user(user):
    response = requests.post(f"{BASE_URL}/users", json=user)
    assert response.status_code == 200
    assert response.json()["name"] == user["name"]
    assert response.json()["job"] == user["job"]

@pytest.mark.parametrize("user_id, user_data", [(2, {"name": "morpheus", "job": "zion resident"})])
def test_update_user(user_id, user_data):
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=user_data)
    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]
    assert response.json()["job"] == user_data["job"]

@pytest.mark.parametrize("user_id", [2])
def test_delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
