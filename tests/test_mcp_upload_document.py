"""Tests for the packaged MCP server's upload_document tool."""

import base64

import pytest

from billit_mcp import server


@pytest.fixture(autouse=True)
def _billit_env(monkeypatch):
    """build_client() reads credentials from the environment."""
    monkeypatch.setenv("BILLIT_BASE_URL", "https://api.billit.test/v1")
    monkeypatch.setenv("BILLIT_API_KEY", "test-key")
    monkeypatch.setenv("BILLIT_PARTY_ID", "1")


@pytest.mark.asyncio
async def test_upload_document_sends_base64_file(monkeypatch, tmp_path):
    """The file itself must be sent, base64 encoded, inside a nested File object.

    Regression test: the tool used to post the *path* instead of the bytes,
    which the Billit API rejects with TheFileCannotBeEmpty.
    """
    pdf = tmp_path / "invoice.pdf"
    pdf.write_bytes(b"%PDF-1.4 fake")

    captured = {}

    async def fake_request(self, method, endpoint, **kwargs):
        captured["method"] = method
        captured["endpoint"] = endpoint
        captured["json"] = kwargs.get("json")
        return {"success": True, "data": 123, "error": None, "error_code": None}

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    result = await server.upload_document(
        str(pdf),
        {"DocumentDate": "2026-04-28T00:00:00", "Tags": ["invoice"]},
    )

    assert result["data"] == 123
    assert captured["method"] == "POST"
    assert captured["endpoint"] == "/documents"

    body = captured["json"]
    assert body["File"]["FileName"] == "invoice.pdf"
    assert body["File"]["MimeType"] == "application/pdf"
    assert base64.b64decode(body["File"]["FileContent"]) == b"%PDF-1.4 fake"
    assert body["DocumentDate"] == "2026-04-28T00:00:00"
    assert body["Tags"] == ["invoice"]
    assert "file_path" not in body


@pytest.mark.asyncio
async def test_upload_document_without_metadata(monkeypatch, tmp_path):
    """metadata is optional."""
    pdf = tmp_path / "plain.pdf"
    pdf.write_bytes(b"data")

    captured = {}

    async def fake_request(self, method, endpoint, **kwargs):
        captured["json"] = kwargs.get("json")
        return {"success": True, "data": None, "error": None, "error_code": None}

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    await server.upload_document(str(pdf))

    assert set(captured["json"]) == {"File"}


@pytest.mark.asyncio
async def test_upload_document_file_overrides(monkeypatch, tmp_path):
    """A nested File key in metadata overrides the derived file fields."""
    pdf = tmp_path / "derived-name.pdf"
    pdf.write_bytes(b"data")

    captured = {}

    async def fake_request(self, method, endpoint, **kwargs):
        captured["json"] = kwargs.get("json")
        return {"success": True, "data": None, "error": None, "error_code": None}

    monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)

    await server.upload_document(str(pdf), {"File": {"FileName": "chosen.pdf"}})

    assert captured["json"]["File"]["FileName"] == "chosen.pdf"
    assert captured["json"]["File"]["MimeType"] == "application/pdf"


@pytest.mark.asyncio
async def test_upload_document_missing_file():
    """A missing file fails fast, before any API call."""
    with pytest.raises(ValueError, match="File not found"):
        await server.upload_document("/definitely/not/here.pdf")
