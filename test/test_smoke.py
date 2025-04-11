import pytest
import requests

from utils.fast_api_app import FastApiApp

@pytest.fixture(scope='function')
def app(env: str):
    return FastApiApp(env)

def test_service_status(app: FastApiApp) -> None:
    response = app.get_status()
    assert response.status_code == 200
    assert response.json() == {'database': True}
