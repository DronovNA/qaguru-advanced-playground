import requests
import pytest

@pytest.mark.parametrize("page, size", [
    (1, 5),
    (2, 5),
    (3, 5),
    (1, 10),
    (2, 10)
])
def test_pagination_response(app_url: str, page: int, size: int):
    """Проверяем, что в ответе присутствуют page и size с правильными значениями."""
    page, size = 2, 5
    response = requests.get(f"{app_url}/api/users", params={"page": page, "size": size})
    assert response.status_code == 200
    data = response.json()

    assert "page" in data, "В ответе отсутствует поле 'page'"
    assert "size" in data, "В ответе отсутствует поле 'size'"
    assert data["page"] == page, f"Ожидалось page={page}, а в ответе {data['page']}"
    assert data["size"] == size, f"Ожидалось size={size}, а в ответе {data['size']}"


def test_pagination_response_structure(app_url: str):
    """Проверяем, что в ответе есть все ожидаемые поля."""
    response = requests.get(f"{app_url}/api/users", params={"page": 1, "size": 5})
    assert response.status_code == 200
    data = response.json()

    expected_keys = {"page", "size", "total", "pages", "items"}
    assert expected_keys.issubset(data.keys()), f"Отсутствуют ключи: {expected_keys - data.keys()}"

@pytest.mark.parametrize("page, size", [(1, 5), (2, 10), (3, 3)])
def test_pagination_page_size_values(app_url: str, page: int, size: int):
    """Проверяем, что в ответе `page` и `size` соответствуют запрошенным параметрам."""
    response = requests.get(f"{app_url}/api/users", params={"page": page, "size": size})
    assert response.status_code == 200
    data = response.json()

    assert data["page"] == page, f"Ожидалось page={page}, а в ответе {data['page']}"
    assert data["size"] == size, f"Ожидалось size={size}, а в ответе {data['size']}"

@pytest.mark.parametrize("page, size", [(1, 5), (2, 5), (3, 2)])
def test_pagination_item_count(app_url: str, page: int, size: int):
    """Проверяем, что количество элементов на странице соответствует `size`."""
    response = requests.get(f"{app_url}/api/users", params={"page": page, "size": size})
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) == min(size, data["total"] - (page - 1) * size), "Некорректное количество элементов на странице"

def test_pagination_data_changes(app_url: str):
    """Проверяем, что страницы содержат разные элементы (уникальные ID)."""
    response_page_1 = requests.get(f"{app_url}/api/users", params={"page": 1, "size": 5})
    response_page_2 = requests.get(f"{app_url}/api/users", params={"page": 2, "size": 5})

    assert response_page_1.status_code == 200, f"Unexpected status: {response_page_1.status_code}"
    assert response_page_2.status_code == 200, f"Unexpected status: {response_page_2.status_code}"

    data_page_1 = response_page_1.json()
    data_page_2 = response_page_2.json()

    ids_page_1 = [user["id"] for user in data_page_1["items"]]
    ids_page_2 = [user["id"] for user in data_page_2["items"]]

    assert len(ids_page_1) == len(set(ids_page_1)), "На первой странице есть дублирующиеся данные"
    assert len(ids_page_2) == len(set(ids_page_2)), "На второй странице есть дублирующиеся данные"

    assert not set(ids_page_1) & set(ids_page_2), "Данные на страницах не должны пересекаться"

@pytest.mark.parametrize("total, size, expected_pages", [(12, 5, 3), (12, 6, 2), (12, 10, 2), (12, 12, 1)])
def test_pagination_total_pages(app_url: str, total: int, size: int, expected_pages: int):
    """Проверяем, что поле `pages` рассчитано корректно."""
    response = requests.get(f"{app_url}/api/users", params={"page": 1, "size": size})
    assert response.status_code == 200
    data = response.json()

    assert data["pages"] == expected_pages, f"Ожидалось {expected_pages} страниц, а в ответе {data['pages']}"


