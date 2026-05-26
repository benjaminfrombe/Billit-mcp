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

- [x] Split the Billit MCP review stack for maintainability (2026-05-26):
  extracted a shared invoice workflow for local API-key and hosted OAuth
  draft/send safety, split the local runtime facade into focused services,
  thinned hosted tool registration, split read-only canary modules, and added a
  source-size quality guard.
- [x] Implemented the new local/private API-key MCP runtime (2026-05-26):
  `python -m billit_mcp` now exposes only curated API-key tools, disables
  `ContextPartyID`, rejects raw OData passthrough, uses local redacted audit,
  local confirmation challenges, idempotency records, write/send gates, and a
  sandbox-first canary that proves curated behavior and write blocking.
- [x] Wrote the API-key local runtime plan and concise `/goal` prompt
  (2026-05-26), including the local live-data canary acceptance gate and the
  decision to remove raw legacy MCP tools from the user-facing stdio surface.
- [x] Remediated hosted OAuth MVP review blockers (2026-05-26): removed
  production ORM schema mutation, replaced the live-metadata Alembic revision
  with explicit DDL, made `/readyz` check DB plus migration head, staged Billit
  OAuth activation behind company sync, deactivated stale companies, guarded
  confirmation consumption, added send revalidation, persisted idempotency
  outcomes, and moved hosted tool audit/API calls through shared runtime
  helpers.
- [x] Implemented the hosted OAuth MCP MVP scaffold (2026-05-26): preserved
  stdio mode, added Streamable HTTP `/mcp`, MCP OAuth, Billit OAuth grant
  persistence, company authorization, curated hosted tools, confirmation
  challenges, redacted audit tables, hosted canary mode, and AWS App Runner
  Terraform project.
- [x] Copied and cleaned the downloaded Billit docs snapshot (2026-05-26):
  regenerated `billit_docs_markdown/` from `/Users/olivierdebeufderijcker/Downloads/billit_docs`,
  skipped crawler 404/duplicate artifacts, added QMD frontmatter, and grouped
  164 source pages into category hubs.
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
- The packaged MCP server now registers only the curated local API-key tools.
  The legacy FastAPI adapter exposes a broader route surface and should be
  documented separately.
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
- Keep upstream Billit docs in `billit_docs_markdown/` as source references
  with QMD frontmatter and category hubs; project behavior belongs in `docs/`.
- Hosted OAuth mode must stay structurally separate from local API-key mode:
  no `BillitSettings.from_env()`, no legacy raw tool registration, and every
  hosted Billit call must validate explicit `company_party_id`.
- Hosted production schema changes must run through Alembic before App Runner
  traffic. App startup stays uvicorn-only; `/readyz` is the enforcement point.
- Invoice send confirmation must be treated as a signed snapshot, not current
  truth. Confirm send must refetch Billit state, recompute the operation hash,
  then atomically consume the challenge before calling Billit.
- API-key mode should be a new curated local/private runtime, not a raw legacy
  tool fallback. OAuth remains the hosted/public connector path.
- Local API-key writes require `accountInformation` to verify the configured
  `BILLIT_PARTY_ID`; reads can continue with warnings when company-list
  parsing is inconclusive.
