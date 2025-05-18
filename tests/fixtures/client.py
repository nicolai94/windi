import pytest
from httpx import AsyncClient, ASGITransport

from starlette.testclient import TestClient

from src.main import app
from src.storage.models.db_helper import db_connector


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[db_connector.session_getter] = override_get_db
    test_api_client = TestClient(app)

    yield test_api_client
    del app.dependency_overrides[db_connector.session_getter]


@pytest.fixture(scope="function")
async def async_client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[db_connector.session_getter] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    del app.dependency_overrides[db_connector.session_getter]
