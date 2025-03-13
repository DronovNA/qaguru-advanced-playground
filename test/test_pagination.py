import requests
import pytest

@pytest.mark.parametrize("page, size, expected_count", [
    (1, 5, 5),  # Первая страница, 5 элементов
    (2, 5, 5),  # Вторая страница, 5 элементов
    (3, 5, 2),  # Третья страница, оставшиеся 2 элемента
    (1, 10, 10),  # Одна большая страница
    (2, 10, 2)   # Вторая страница, оставшиеся 2 элемента
])
def test_get_users_pagination(app_url: str, page: int, size: int, expected_count: int) -> None:
    response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": size})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == expected_count
    assert data["total"] == 12
    assert data["pages"] == (12 // size + (1 if 12 % size > 0 else 0))

def test_pagination_data_changes(app_url: str) -> None:
    """Проверяем, что страницы содержат разные данные"""
    response_page_1 = requests.get(f"{app_url}/api/users", params={"page": 1, "size": 5}).json()
    response_page_2 = requests.get(f"{app_url}/api/users", params={"page": 2, "size": 5}).json()
    assert response_page_1["items"] != response_page_2["items"]