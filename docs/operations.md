---
title: "Billit MCP - Operations Runbook"
updated: 2026-05-26
---

# Billit MCP Operations Runbook

This runbook covers deployment, package publishing, public release checks,
credential rotation, and troubleshooting for Billit MCP.

## Billit MCP Local Operation

Run the packaged MCP server locally:

```bash
uv run python -m billit_mcp
```

Run the legacy FastAPI adapter locally:

```bash
uv run uvicorn server:app --reload
```

The MCP process communicates over stdio and will appear idle when started by
hand. That is normal; it is waiting for an MCP client to send protocol
messages.

## Billit MCP Docker Operation

Build and run the MCP stdio server:

```bash
docker build -t billit-mcp .
docker run --rm -i --env-file .env billit-mcp
```

Do not publish Docker images that bake in `.env` files. Pass credentials at
runtime through environment variables or a secret manager.

## Billit MCP PyPI Packaging

Build the package:

```bash
uv build
```

Publish only from a clean working tree and only after:

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy billit src tests
uv run lint-imports
uv run pytest -q
```

Store PyPI tokens outside the repository. `.pypirc` is ignored and should never
be committed.

## Billit MCP Public Release Checklist

Before making a repository public or publishing a package:

1. Run a tracked-file secret scan for API keys and package tokens.
2. Confirm `.env`, `.pypirc`, local customer exports, and cache folders are
   ignored.
3. Confirm docs do not contain real Party IDs, customer names, invoices, or
   account-specific analysis.
4. Run `git ls-files '*.md'` and check that public docs are current.
5. Run `uv run ruff check .` and `uv run pytest -q`.

If a secret was committed in the past, rotate it. Squashing public history does
not guarantee every previous clone or log is gone.

## Billit MCP Credential Rotation

Rotate Billit keys through the Billit UI, then update the MCP client
environment. On macOS, update Keychain first and hydrate local `.env` after:

```bash
security add-generic-password -a "$USER" -s BILLIT_API_KEY_K4K -w "new-value" -U
security find-generic-password -w -s BILLIT_API_KEY_K4K
```

Use separate Keychain services for production and sandbox keys. This avoids
accidentally running tests or demos against production.

## Billit MCP Local Live Canary

Run the local canary after endpoint or composite-helper changes. It is
read-only, sandbox-first, refused in CI, and writes sanitized status/count
evidence under `.local/billit-live-canary/`.

```bash
BILLIT_API_KEY="$(security find-generic-password -w -s BILLIT_SANDBOX_API_KEY_K4K)" \
BILLIT_BASE_URL=https://api.sandbox.billit.be/v1 \
BILLIT_PARTY_ID="$BILLIT_PARTY_ID" \
uv run python scripts/local/live_billit_canary.py --read-only
```

Do not commit `.local/` canary evidence. The report intentionally excludes API
keys, customer names, emails, invoice bodies, and raw Billit response payloads.

## Billit MCP Troubleshooting Startup Failures

Missing required environment variables raise a runtime error when the first
client is built. Check `BILLIT_API_KEY`, `BILLIT_BASE_URL`, and
`BILLIT_PARTY_ID`.

Invalid log levels fall back to `INFO` in `src/billit_mcp/__main__.py`. If logs
are unexpectedly quiet, set `LOG_LEVEL=DEBUG` and restart the MCP client.

MCP client configuration changes usually require a full client restart. Reload
or reconnect behavior is client-specific and should not be trusted for
credential changes.

## Billit MCP Troubleshooting Billit API Failures

`REQUEST_ERROR` means the HTTP client failed before receiving a Billit
response. Check network access, base URL, TLS interception, and timeout.

Authentication failures usually mean the key, base URL, or party ID do not
belong together. Re-check sandbox versus production configuration first.

Patch failures on orders or parties often mean the payload contains fields that
Billit does not allow to be changed after creation. Prefer creating a corrected
order over patching immutable invoice line, VAT, or customer fields.
