import pytest
from starlette.testclient import TestClient
from foodshareapp.app.application import app


@pytest.fixture(scope="session")
def setup_test_database(test_database):
    """Ensure the test database is available for all tests."""
    yield test_database


@pytest.fixture(scope="function")
def client(setup_test_database):
    """Provides a synchronous test client for FastAPI using the test database."""
    return TestClient(app)
