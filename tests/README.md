---
title: "Billit MCP - Test Suite Guide"
updated: 2026-05-26
---

# Billit MCP Test Suite Guide

The test suite covers the shared Billit client, the legacy FastAPI route
adapter, local composite helpers, and live read-only checks. Most tests do not
require Billit credentials because they monkeypatch `BillitAPIClient.request`
or mock outbound HTTP with `respx`.

## Billit MCP Unit and Route Tests

Run the standard gate:

```bash
uv run pytest -q
```

The standard suite includes route tests for accounts, accountant feeds, AI
composites, documents, financial transactions, GL accounts, orders, parties,
Peppol, products, reports, OCR processing, webhooks, and the shared client.
Live tests are collected but skipped unless `--live` is provided.

## Billit MCP Ruff Gate

Run Ruff before committing:

```bash
uv run ruff format --check .
uv run ruff check .
```

Ruff uses the repository's Motium-style selector set in `pyproject.toml`.
Keep documentation examples readable, but do not weaken lint config for test
or implementation shortcuts.

## Billit MCP Live Canary Test

The live pytest path is a thin wrapper around the local read-only canary:

```bash
uv run pytest tests/test_live_integration.py -q --live
```

Use sandbox credentials by default. Prefer canary-specific sandbox variables:

```env
BILLIT_SANDBOX_API_KEY_K4K=your-sandbox-api-key
BILLIT_SANDBOX_PARTY_ID=your-sandbox-party-id
```

Do not run live tests against production unless you have intentionally selected
production credentials and understand the side effects. The current canary has
no write probes and records only sanitized status/count evidence.

## Billit MCP Test Authoring Pattern

For FastAPI route tests, use `httpx.ASGITransport(app=app)` and monkeypatch the
client request method:

```python
async def fake_request(self, method, endpoint, **kwargs):
    assert method == "GET"
    assert endpoint == "/orders"
    return {"success": True, "data": [], "error": None, "error_code": None}

monkeypatch.setattr("billit.client.BillitAPIClient.request", fake_request)
```

Normal tests install a guard that fails unmocked `BillitAPIClient.request`
calls. Direct client tests that intentionally exercise the request method must
use `respx` and the `allow_billit_request` marker.

For direct client tests, set `BILLIT_API_KEY`, `BILLIT_BASE_URL`, and
`BILLIT_PARTY_ID` with `monkeypatch.setenv`, then mock HTTP responses with
`respx`.

## Billit MCP Test Safety Rules

- Keep ordinary tests credential-free.
- Use standard response envelopes in mocks.
- Assert the exact Billit endpoint path when a route proxies the API.
- Keep live tests on the shared canary runner; do not add ad hoc live probes
  that bypass its read-only guard.
- Avoid putting real customer names, invoice IDs, or API payloads into expected
  values.
