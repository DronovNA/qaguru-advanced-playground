import requests

def test_service_status(app_url: str) -> None:
    response = requests.get(f"{app_url}/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}