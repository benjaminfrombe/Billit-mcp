---
title: "Billit MCP - Agent Instructions"
updated: 2026-05-26
---

# Billit MCP Agent Instructions

Before changing this repository, read [Documentation Index](docs/index.md) and
[Architecture and Data Flow](docs/architecture.md). The current source of truth
is the codebase, not older generated plans or historical task logs.

## Billit MCP Runtime Rules

- The canonical runtime is `python -m billit_mcp`.
- `src/billit_mcp/server.py` is the packaged MCP stdio server.
- `server.py` and `billit/tools/` are the legacy FastAPI adapter used for local
  HTTP development and route tests.
- `billit/client.py` is the only shared Billit REST client. Keep the response
  envelope `{success, data, error, error_code}` stable.
- Keep credentials in environment variables or macOS Keychain, never in tracked
  files.

## Billit MCP Documentation Rules

- Treat project Markdown without current frontmatter as stale.
- Every maintained Markdown file should include `title` and `updated`
  frontmatter for QMD retrieval.
- Prefer focused docs under `docs/` over large root-level files.
- Do not duplicate upstream Billit API reference content into project docs.
  Link to `billit_docs_markdown/` instead.
- When changing behavior, update the nearest relevant doc and tests in the
  same change.

## Billit MCP Development Checks

Run these before handing off code or documentation changes:

```bash
uv run ruff check .
uv run pytest -q
```

Run live tests only when credentials and environment are intentionally selected:

```bash
uv run pytest tests/test_live_integration.py -q --live
```

That live pytest path is a wrapper around the local read-only canary. Do not add
separate ad hoc live probes that bypass `scripts/local/live_billit_canary.py`.

## Olivier Drafting Voice

When drafting or rewriting anything meant to be sent as Olivier, use the
`olivier-drafting-voice` skill and run a `stop-slop` pass before presenting it.
This applies to X/Twitter, quote tweets, LinkedIn, email, WhatsApp, Teams,
Slack, stakeholder updates, sales notes, and any other outbound copy.

Default to concrete, slightly informal, situation-specific writing. Preserve
the user's raw phrasing when it sounds natural. Avoid polished AI-writing
tropes, especially `it's not X, it's Y`, `the real unlock is`,
`this matters because`, `here's the thing`, `at its core`, dramatic reveals,
tidy three-part structures, and quote-card endings.
