"""Tests for document domain endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient
from server import app


@pytest.mark.asyncio
async def test_list_documents(monkeypatch):
    """Test listing documents."""
    expected_response = {
        "success": True,
        "data": [
            {
                "DocumentID": 123,
                "FileName": "report.pdf",
                "FileSize": 102400,
                "CreatedDate": "2024-01-15T10:00:00Z",
            }
        ],
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/documents"
        params = kwargs.get("params", {})
        assert params.get("$skip") == 0
        assert params.get("$top") == 120
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/documents")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_list_documents_with_filter(monkeypatch):
    """Test listing documents with OData filter."""
    expected_response = {"success": True, "data": [], "error": None, "error_code": None}

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/documents"
        params = kwargs.get("params", {})
        assert params.get("$filter") == "FileName eq 'test.pdf'"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/documents?odata_filter=FileName eq 'test.pdf'")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_upload_document(monkeypatch):
    """Test uploading a document."""
    expected_response = {
        "success": True,
        "data": {
            "DocumentID": 456,
            "FileName": "upload.pdf",
            "FileID": "file-789",
            "UploadStatus": "Success",
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "POST"
        assert endpoint == "/documents"
        assert "files" in kwargs
        assert "data" in kwargs
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # For FastAPI file upload with additional fields, we need to send the metadata as form data
        files = {"file": ("upload.pdf", b"test content", "application/pdf")}
        # Metadata needs to be JSON string in form data
        data = {"metadata": '{"description": "Test document"}'}
        response = await client.post("/documents", files=files, data=data)
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_get_document(monkeypatch):
    """Test getting a specific document."""
    expected_response = {
        "success": True,
        "data": {
            "DocumentID": 123,
            "FileName": "report.pdf",
            "FileSize": 102400,
            "ContentType": "application/pdf",
            "CreatedDate": "2024-01-15T10:00:00Z",
            "Metadata": {"type": "report", "year": "2024"},
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/documents/123"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/documents/123")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_download_file(monkeypatch):
    """Test downloading a file."""
    expected_response = {
        "success": True,
        "data": {
            "Content": "base64encodedcontent==",
            "ContentType": "application/pdf",
            "FileName": "report.pdf",
            "FileSize": 102400,
        },
        "error": None,
        "error_code": None,
    }

    async def fake_request(self, method, endpoint, **kwargs):
        assert method == "GET"
        assert endpoint == "/files/file-789"
        return expected_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/files/file-789")
        assert response.status_code == 200
        assert response.json() == expected_response


@pytest.mark.asyncio
async def test_document_error_handling(monkeypatch):
    """Test error handling for document operations."""
    error_response = {
        "success": False,
        "data": None,
        "error": "Document not found",
        "error_code": "NOT_FOUND",
    }

    async def fake_request(self, method, endpoint, **kwargs):
        return error_response

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/documents/999")
        assert response.status_code == 200
        assert response.json() == error_response
