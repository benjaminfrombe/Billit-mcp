"""Tests for to_process (OCR) domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from server import app


@pytest.mark.asyncio
async def test_submit_document_for_processing(monkeypatch):
    """Test submitting a document for OCR processing."""
    expected_response = {
        "success": True,
        "data": {
            "UploadID": "upload-123",
            "Status": "Queued",
            "EstimatedProcessingTime": "2-5 minutes",
            "FileName": "supplier_invoice.pdf"
        },
        "error": None,
        "error_code": None
    }
    
    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/toProcess"
        assert "files" in kwargs
        assert "data" in kwargs
        return expected_response
    
    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        files = {"file": ("supplier_invoice.pdf", b"test content", "application/pdf")}
        data = {"metadata": '{"document_type": "supplier_invoice", "priority": "normal"}'}
        response = await client.post("/process", files=files, data=data)
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_update_processing_request(monkeypatch):
    """Test updating a document processing request."""
    expected_response = {
        "success": True,
        "data": {
            "UploadID": "upload-123",
            "Status": "Processing",
            "UpdatedFields": ["priority", "expected_supplier"],
            "Message": "Processing request updated successfully"
        },
        "error": None,
        "error_code": None
    }
    
    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "PATCH"
        assert endpoint == "/toProcess/upload-123"
        data = kwargs.get("json", {})
        assert data["priority"] == "high"
        assert data["expected_supplier"] == "ACME Corp"
        return expected_response
    
    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch("/process/upload-123", json={
            "priority": "high",
            "expected_supplier": "ACME Corp"
        })
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_cancel_processing_request(monkeypatch):
    """Test canceling a document processing request."""
    expected_response = {
        "success": True,
        "data": {
            "UploadID": "upload-123",
            "Status": "Cancelled",
            "CancelledAt": "2024-01-15T12:00:00Z",
            "Message": "Processing request cancelled successfully"
        },
        "error": None,
        "error_code": None
    }
    
    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "DELETE"
        assert endpoint == "/toProcess/upload-123"
        return expected_response
    
    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/process/upload-123")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_to_process_error_handling(monkeypatch):
    """Test error handling for document processing operations."""
    error_response = {
        "success": False,
        "data": None,
        "error": "Document processing failed: Unsupported file format",
        "error_code": "UNSUPPORTED_FORMAT"
    }
    
    async def fake_request(self, method, endpoint, **kwargs):
        return error_response
    
    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        files = {"file": ("image.jpg", b"test content", "image/jpeg")}
        data = {"metadata": '{}'}
        response = await client.post("/process", files=files, data=data)
        assert response.status_code == 200
        assert response.json() == error_response


@pytest.mark.asyncio
async def test_processing_already_completed(monkeypatch):
    """Test updating an already processed document."""
    error_response = {
        "success": False,
        "data": None,
        "error": "Cannot update completed processing request",
        "error_code": "ALREADY_COMPLETED"
    }
    
    async def fake_request(self, method, endpoint, **kwargs):
        return error_response
    
    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.patch("/process/upload-456", json={
            "priority": "high"
        })
        assert response.status_code == 200
        assert response.json() == error_response