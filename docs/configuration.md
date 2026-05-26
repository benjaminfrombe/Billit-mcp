---
title: "Billit MCP - Configuration Reference"
updated: 2026-05-26
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

`BILLIT_PARTY_ID` is the Billit company Party ID used in the `partyID` header.
It is required even for read operations because Billit scopes requests by
company.

## Billit MCP Optional Environment Variables

`BILLIT_CONTEXT_PARTY_ID` sets the `ContextPartyID` header for accountant use
cases. Leave it empty for ordinary company-scoped usage.

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
BILLIT_CONTEXT_PARTY_ID=
RATE_LIMIT_PER_MINUTE=50
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

Do not use production `BILLIT_PARTY_ID` with sandbox keys or sandbox base URLs.
Credential/base-url mismatches usually produce authentication or not-found
errors that look like application bugs.

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
