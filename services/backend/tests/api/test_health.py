import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.unit
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"
    assert data["environment"] == settings.ENVIRONMENT
    assert data["project_name"] == settings.PROJECT_NAME
