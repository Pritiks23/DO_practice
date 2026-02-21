"""Tests for health check endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test suite for health check endpoints."""

    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint returns correct status."""
        response = await client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime" in data
        assert "version" in data
        assert isinstance(data["uptime"], (int, float))

    async def test_readiness_check(self, client: AsyncClient):
        """Test readiness check endpoint returns correct status."""
        response = await client.get("/api/v1/ready")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ready"
        assert "timestamp" in data
