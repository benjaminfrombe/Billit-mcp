---
title: "Billit MCP Task Log"
updated: 2026-05-26
---

# Billit MCP Task Log

## TODO

- [ ] Keep `docs/mcp-tools.md` synchronized with `src/billit_mcp/server.py`
  whenever MCP tools are added, removed, or renamed.
- [ ] Decide whether the legacy FastAPI adapter remains supported public API,
  moves to development-only status, or is removed.

## DONE

- [x] Implemented the Billit MCP quality remediation and Motium-style CI
  migration (2026-05-26): hermetic tests, MCP lifecycle cleanup, shared
  composite helpers, endpoint drift fixes, uv/Hatch migration, CI gates, and
  documentation updates.
- [x] Resolved thermo-nuclear review follow-ups (2026-05-26): single
  read-only live canary contract, explicit client settings for canary runs,
  centralized pagination clamping, and simplified composite query helpers.
- [x] Added and ran the local read-only live-data Billit sandbox canary
  (2026-05-26): sanitized evidence written under ignored `.local/` with
  `/reports`, `/financialTransactions`, and shared composite helper proof.
- [x] Wrote the end-to-end quality remediation plan and concise `/goal` prompt
  (2026-05-26), including the local live-data canary acceptance gate.
- [x] Full repository documentation refresh from the current codebase
  (2026-05-26): rewrote public docs, removed stale/private docs, added
  code-derived architecture/runtime/testing/operations docs, and added
  frontmatter to maintained Markdown.
- [x] Documentation refresh validation suite (2026-05-26): `poetry install`,
  `poetry run ruff check .`, `poetry run pytest -q`, `git diff --check`,
  frontmatter check, and local Markdown link check all completed.
- [x] Code quality remediation plan (2026-05-26): Ruff clean, pytest baseline
  green except live skips, tracked credential files removed, and canonical MCP
  entrypoint restored.
- [x] AGENTS.md updated with Olivier Drafting Voice instructions
  (2026-05-26).

## Learnings

- Canonical runtime is `python -m billit_mcp` or `uv run billit-mcp`;
  root `server.py` is a legacy FastAPI/local-test adapter.
- The packaged MCP server currently registers 44 tools. The legacy FastAPI
  adapter exposes a broader route surface and should be documented separately.
- Keep `.env`, `.pypirc`, Billit API keys, and package tokens out of git; use
  environment variables, MCP client config, macOS Keychain, or another secret
  manager.
- Public docs should point at `https://github.com/olivier-motium/Billit-mcp`.
- A freshly created environment should be installed with `uv sync --locked`
  before interpreting pytest import errors.
- The remediation canary must use live Billit data locally, write only
  sanitized evidence under `.local/`, and stay out of CI/default pytest.
- The live pytest path should stay a wrapper around the shared canary runner,
  not a second broad live integration suite.
- Billit sandbox accepts `/reports` for report listing; `/report` fails.
- Billit list/composite helpers should cap `$top` at 120; sandbox rejects
  larger values such as `$top=500` for the filtered order queries used here.
