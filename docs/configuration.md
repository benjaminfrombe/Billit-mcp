---
title: "Billit MCP - Configuration Reference"
updated: 2026-05-27
---

# Billit MCP Configuration Reference

Billit MCP is configured entirely through environment variables. Local runs
also load a `.env` file from the repository root through `python-dotenv`.

## Billit MCP Required Environment Variables

`BILLIT_API_KEY` is the Billit API key used for `apiKey` authentication. Keep
this value in a secret manager, MCP client environment block, macOS Keychain,
or ignored `.env` file.

`BILLIT_BASE_URL` selects the Billit environment. Use
`https://api.billit.be/v1` for production and
`https://api.sandbox.billit.be/v1` for sandbox.

`BILLIT_PARTY_ID` is the explicit Billit company Party ID used in the `PartyID`
header. It is required even for read operations because Billit scopes requests
by company.

## Billit MCP Optional Environment Variables

`BILLIT_MCP_LOCAL_ALLOW_WRITES` enables local sales-invoice draft creation when
set to `1`. The default is disabled.

`BILLIT_MCP_LOCAL_ALLOW_SENDS` enables the local confirmation-gated invoice
send workflow when set to `1`. The default is disabled.

`BILLIT_CONTEXT_PARTY_ID` is ignored by the curated local MCP runtime.
`ContextPartyID` is disabled for this MVP. The legacy FastAPI adapter can still
build raw env-derived clients for local route experiments, but MCP stdio calls
do not send this header.

`RATE_LIMIT_PER_MINUTE` controls the shared token bucket. The default is `50`.
Raise it only if the Billit account and integration contract allow it.

`LOG_LEVEL` controls package logging in `src/billit_mcp/__main__.py`. It
defaults to `INFO` and accepts standard Python logging levels such as `DEBUG`,
`INFO`, `WARNING`, and `ERROR`.

## Billit MCP Local .env Template

```env
BILLIT_API_KEY=your-billit-api-key
BILLIT_BASE_URL=https://api.billit.be/v1
BILLIT_PARTY_ID=your-company-party-id
RATE_LIMIT_PER_MINUTE=50
BILLIT_MCP_LOCAL_ALLOW_WRITES=0
BILLIT_MCP_LOCAL_ALLOW_SENDS=0
LOG_LEVEL=INFO
```

The repository `.gitignore` excludes `.env`. Keep file permissions strict on
shared machines:

```bash
chmod 600 .env
```

## Billit MCP Sandbox Configuration

Use sandbox credentials with the sandbox base URL:

```env
BILLIT_API_KEY=your-sandbox-api-key
BILLIT_BASE_URL=https://api.sandbox.billit.be/v1
BILLIT_PARTY_ID=your-sandbox-party-id
```

For the local API-key live canary, use sandbox-specific variables. The canary
accepts only `BILLIT_SANDBOX_API_KEY_K4K` from env or macOS Keychain service
`BILLIT_SANDBOX_API_KEY_K4K`, plus `BILLIT_SANDBOX_PARTY_ID` or
`BILLIT_PARTY_ID`:

```env
BILLIT_SANDBOX_API_KEY_K4K=your-sandbox-api-key
BILLIT_SANDBOX_PARTY_ID=your-sandbox-party-id
```

Do not use production `BILLIT_PARTY_ID` with sandbox keys or sandbox base URLs.
Credential/base-url mismatches usually produce authentication or not-found
errors that look like application bugs.

## Billit MCP Local State

The local API-key runtime stores redacted audit events, confirmation
challenges, and idempotency records in ignored SQLite state under `.local/`.
The default path is:

```text
.local/billit-mcp-api-key-state.db
```

Override it only for tests or isolated local runs:

```env
BILLIT_MCP_LOCAL_STATE_DB=.local/my-billit-state.db
```

The state database must not contain API keys, raw customer payloads, raw
invoice payloads, files, or webhook bodies.

## Billit MCP macOS Keychain Pattern

On macOS, store keys as generic passwords and hydrate `.env` only locally:

```bash
security add-generic-password -a "$USER" -s BILLIT_API_KEY_K4K -w "..."
security find-generic-password -w -s BILLIT_API_KEY_K4K
```

For sandbox keys, use a separate service name such as
`BILLIT_SANDBOX_API_KEY_K4K`. Keeping production and sandbox secrets separate
prevents accidental production writes during live testing.

## Billit MCP Secret Handling Rules

Never commit `.env`, `.pypirc`, API keys, package publish tokens, exported
customer data, invoice payloads, or terminal logs containing live Billit data.

If a secret was ever committed, rotate it even if the public repository history
has since been squashed. GitHub, package mirrors, local clones, CI logs, and
chat transcripts can preserve old values outside the current branch.
