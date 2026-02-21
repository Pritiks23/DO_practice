"""Tests for data API endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestDataEndpoints:
    """Test suite for data API endpoints."""
    
    created_record_id = None
    
    async def test_ingest_data_success(self, client: AsyncClient):
        """Test successful data ingestion."""
        test_data = {
            "data": {
                "sensor": "temperature",
                "value": 25.5,
                "unit": "celsius"
            },
            "metadata": {
                "source": "sensor-001"
            }
        }
        
        response = await client.post("/api/v1/data", json=test_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["success"] is True
        assert "id" in data["data"]
        assert "timestamp" in data["data"]
        assert data["data"]["processed"] is False
        assert data["data"]["data"] == test_data["data"]
        assert data["data"]["metadata"] == test_data["metadata"]
        
        # Store for later tests
        TestDataEndpoints.created_record_id = data["data"]["id"]
    
    async def test_ingest_data_missing_data_field(self, client: AsyncClient):
        """Test data ingestion with missing data field."""
        response = await client.post("/api/v1/data", json={})
        
        assert response.status_code == 422  # Pydantic validation error
    
    async def test_ingest_data_invalid_data_type(self, client: AsyncClient):
        """Test data ingestion with invalid data type."""
        response = await client.post("/api/v1/data", json={"data": "not an object"})
        
        # Pydantic will raise a 422 for validation errors
        assert response.status_code == 422
    
    async def test_get_specific_record(self, client: AsyncClient):
        """Test retrieving a specific data record."""
        # First create a record
        test_data = {
            "data": {"test": "value"},
            "metadata": {"source": "test"}
        }
        create_response = await client.post("/api/v1/data", json=test_data)
        record_id = create_response.json()["data"]["id"]
        
        # Now retrieve it
        response = await client.get(f"/api/v1/data/{record_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["id"] == record_id
    
    async def test_get_non_existent_record(self, client: AsyncClient):
        """Test retrieving a non-existent record returns 404."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.get(f"/api/v1/data/{fake_id}")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "error" in data
        assert data["error"]["statusCode"] == 404
    
    async def test_get_all_data(self, client: AsyncClient):
        """Test retrieving all data records."""
        response = await client.get("/api/v1/data")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert isinstance(data["data"], list)
        assert "pagination" in data
        assert "stats" in data
        assert "total" in data["stats"]
        assert "processed" in data["stats"]
        assert "unprocessed" in data["stats"]
    
    async def test_get_all_data_pagination(self, client: AsyncClient):
        """Test data retrieval with pagination."""
        response = await client.get("/api/v1/data?limit=5&offset=0")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["pagination"]["limit"] == 5
        assert data["pagination"]["offset"] == 0
    
    async def test_process_data(self, client: AsyncClient):
        """Test processing a data record."""
        # First create a record
        test_data = {
            "data": {"test": "value"},
            "metadata": {"source": "test"}
        }
        create_response = await client.post("/api/v1/data", json=test_data)
        record_id = create_response.json()["data"]["id"]
        
        # Now process it
        response = await client.post(f"/api/v1/data/{record_id}/process")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["processed"] is True
        assert "processingTimestamp" in data["data"]
        assert "processingResult" in data["data"]
        assert data["data"]["processingResult"]["status"] == "success"
    
    async def test_process_non_existent_record(self, client: AsyncClient):
        """Test processing a non-existent record returns 404."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.post(f"/api/v1/data/{fake_id}/process")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "error" in data
        assert data["error"]["statusCode"] == 404
    
    async def test_process_already_processed_record(self, client: AsyncClient):
        """Test processing an already processed record."""
        # First create and process a record
        test_data = {
            "data": {"test": "value"},
            "metadata": {"source": "test"}
        }
        create_response = await client.post("/api/v1/data", json=test_data)
        record_id = create_response.json()["data"]["id"]
        await client.post(f"/api/v1/data/{record_id}/process")
        
        # Process again
        response = await client.post(f"/api/v1/data/{record_id}/process")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["data"]["processed"] is True
    
    async def test_delete_data(self, client: AsyncClient):
        """Test deleting a data record."""
        # First create a record
        test_data = {
            "data": {"test": "value"},
            "metadata": {"source": "test"}
        }
        create_response = await client.post("/api/v1/data", json=test_data)
        record_id = create_response.json()["data"]["id"]
        
        # Now delete it
        response = await client.delete(f"/api/v1/data/{record_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "deleted successfully" in data["message"]
    
    async def test_delete_non_existent_record(self, client: AsyncClient):
        """Test deleting a non-existent record returns 404."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.delete(f"/api/v1/data/{fake_id}")
        
        assert response.status_code == 404
        data = response.json()
        
        assert data["error"]["statusCode"] == 404
    
    async def test_undefined_route(self, client: AsyncClient):
        """Test that undefined routes return 404."""
        response = await client.get("/api/v1/undefined-route")
        
        assert response.status_code == 404
        data = response.json()
        
        assert "error" in data
        assert data["error"]["statusCode"] == 404
