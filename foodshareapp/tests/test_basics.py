from starlette.testclient import TestClient
from starlette import status

from foodshareapp.app.api.application import app


client = TestClient(app)


def test_openapi_json():
    response = client.get("/api/openapi.json")
    assert response.status_code == status.HTTP_200_OK, response.json


def test_doc():
    response = client.get("/api/docs")
    assert response.status_code == status.HTTP_200_OK, response.text


def test_redoc():
    response = client.get("/api/redoc")
    assert response.status_code == status.HTTP_200_OK, response.text


def test_health():
    response = client.get("/api/health")
    assert response.status_code == status.HTTP_200_OK, response.text


def test_echo():
    message = "hello"
    url = "/api/echo/"
    response = client.post(
        url,
        json={
            "message": message,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == message
