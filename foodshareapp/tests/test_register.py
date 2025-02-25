import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from foodshareapp.app.application import app
from foodshareapp.app.api.services.crypto import hash_password, gen_salt

assert isinstance(app, FastAPI)
client = TestClient(app)


@pytest.fixture
def valid_user():
    """Return a valid user payload."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "password": "SecurePass123!",
        "terms": True,
    }


@pytest.fixture
def existing_user():
    """Mock an existing user in the database."""
    return {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "email": "test@example.com",
        "username": "existinguser",
        "firstname": "Existing",
        "lastname": "User",
        "password": "SecurePass123!",
        "salt": gen_salt(),
    }


@pytest.mark.asyncio
async def test_register_success(valid_user):
    """Test successful user registration."""
    with patch(
        "foodshareapp.db.models.user.get_user_by_email", AsyncMock(return_value=None)
    ), patch("foodshareapp.db.models.user.insert_user", AsyncMock()):
        response = client.post("/register", json=valid_user)
        assert response.status_code == 201
        assert "uuid" in response.json()
        assert response.json()["email"] == valid_user["email"]
        assert response.json()["username"] == valid_user["username"]


@pytest.mark.asyncio
async def test_register_existing_email(valid_user, existing_user):
    """Test registering a user with an existing email."""
    with patch(
        "foodshareapp.db.models.user.get_user_by_email",
        AsyncMock(return_value=existing_user),
    ):
        response = client.post("/register", json=valid_user)
        assert response.status_code == 422
        assert response.json()["detail"] == "a user with that email already exists"


@pytest.mark.asyncio
async def test_register_invalid_email():
    """Test registering with an invalid email."""
    invalid_user = {
        "email": "invalid-email",
        "username": "testuser",
        "firstname": "Test",
        "lastname": "User",
        "password": "SecurePass123!",
        "terms": True,
    }
    response = client.post("/register", json=invalid_user)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_fields():
    """Test registering with missing required fields."""
    invalid_user = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "SecurePass123!",
        "terms": True,
    }  # Missing firstname, lastname
    response = client.post("/register", json=invalid_user)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_password_hashing(valid_user):
    """White-box test: password hashing works correctly."""
    salt = gen_salt()
    hashed_password = hash_password(valid_user["password"], salt)

    assert hashed_password != valid_user["password"]  # Ensure password is hashed
    assert isinstance(hashed_password, str)


@pytest.mark.asyncio
async def test_register_password_storage(valid_user):
    """White-box test: hashed password and salt are stored correctly."""
    with patch(
        "foodshareapp.db.models.user.insert_user", AsyncMock()
    ) as mock_insert_user:
        salt = gen_salt()
        valid_user["password"] = hash_password(valid_user["password"], salt)

        response = client.post("/register", json=valid_user)
        assert response.status_code == 201

        mock_insert_user.assert_called_once()
        stored_user = mock_insert_user.call_args[0][0]
        assert stored_user.password != valid_user["password"]
        assert stored_user.salt == salt  # Ensure salt is stored


@pytest.mark.asyncio
async def test_register_without_terms(valid_user):
    """Test registration fails when terms are not accepted."""
    valid_user["terms"] = False
    response = client.post("/register", json=valid_user)
    assert response.status_code == 422  # Assuming terms acceptance is mandatory
