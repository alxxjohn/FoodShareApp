import pytest
from fastapi.testclient import TestClient
import foodshareapp.app.application as app_module

client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    import foodshareapp.db.models.auth as db_user
    import foodshareapp.app.api.services.crypto as crypto
    import foodshareapp.db.utils as db_utils

    mock_get_user_pass(monkeypatch)
    mock_update_functions(monkeypatch, db_user)
    mock_crypto_functions(monkeypatch, crypto)
    mock_db_transaction(app_module, db_utils)

    yield
    app_module.app.dependency_overrides = {}


def mock_get_user_pass(monkeypatch):
    async def mock_get_user_pass(username):
        if username == "alex@test.com":
            return {
                "uuid": "ba177717-21c0-4744-b081-d9d575d4e1d8",
                "email": "alex@test.com",
                "salt": "salt",
                "password": "hashedpassword",
                "bad_login_count": 0,
                "account_locked": False,
            }
        return None

    monkeypatch.setattr("foodshareapp.db.models.auth.get_user_pass", mock_get_user_pass)
    monkeypatch.setattr(
        "foodshareapp.app.api.services.crypto.verify_password", lambda p, h, s: True
    )


def mock_update_functions(monkeypatch, db_user):
    async def noop(*args, **kwargs):
        return None

    monkeypatch.setattr(db_user, "update_bad_login", noop)
    monkeypatch.setattr(db_user, "update_login", noop)


def mock_crypto_functions(monkeypatch, _crypto):
    monkeypatch.setattr(
        "foodshareapp.app.api.routes.auth.verify_password", lambda p, h, s: True
    )
    monkeypatch.setattr(
        "foodshareapp.app.api.routes.auth.create_access_token",
        lambda uuid, expires_delta: "mock-access-token",
    )
    monkeypatch.setattr(
        "foodshareapp.app.api.routes.auth.create_refresh_token",
        lambda uuid: "mock-refresh-token",
    )


def mock_db_transaction(app_module, db_utils):
    class MockDbTransaction:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def commit(self):
            pass

    app_module.app.dependency_overrides[db_utils.db_transaction] = (
        lambda: MockDbTransaction()
    )


def test_login_failure_invalid_user():
    response = client.post(
        "/api/auth/login",
        data={"username": "fake@test.com", "password": "wrong"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 404
