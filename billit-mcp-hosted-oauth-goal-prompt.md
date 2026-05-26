---
title: "Billit MCP - Hosted OAuth Refactor Goal Prompt"
updated: 2026-05-26
---

# Billit MCP Hosted OAuth Refactor Goal Prompt

```text
/goal Implement the Billit MCP hosted OAuth MVP in this repo.

Read AGENTS.md, docs/index.md, docs/architecture.md, docs/mcp-tools.md, billit-mcp-hosted-oauth-refactor-plan.md, and billit-mcp-quality-remediation-plan.md first. Preserve unrelated dirty docs work.

Deliver the MVP from the plan, phased and reviewable:
- preserve local `python -m billit_mcp` stdio mode
- add hosted Streamable HTTP MCP at `/mcp`
- pin/prove an MCP SDK version that supports hosted Streamable HTTP
- split stdio/local runtime from hosted ASGI runtime
- keep root `server.py` and `billit/tools/` as legacy local FastAPI adapter code
- ensure hosted mode cannot import/register raw legacy tools or use `BILLIT_API_KEY`, `BILLIT_PARTY_ID`, or `BillitSettings.from_env()`
- implement MCP OAuth: protected-resource metadata, auth-server metadata, PKCE S256 auth-code flow, token validation, revocation, and scopes
- implement separate Billit OAuth bridge: encrypted grants, Postgres + SQLAlchemy + Alembic, row-locked one-time refresh-token rotation, company sync, and reauthorization_required on refresh failure
- store runtime secrets in AWS Secrets Manager and encrypt token material at rest
- validate `company_party_id` against synced Billit companies before every hosted Billit call
- expose only MVP hosted tools: connection_status, list_companies, search_orders, get_order, resolve_party, lookup_peppol_receiver, invoice.prepare, invoice.create_draft, invoice.prepare_send, invoice.confirm_send, invoice.get_delivery_status
- reject arbitrary OData; compile structured allowlisted filters only
- use server-owned confirmation challenges for invoice sending; never accept generic `confirmed: true`
- add redacted audit for auth, tool calls, confirmations, Billit API calls/errors, and denials
- add AWS infra in `olivier-aws-infra/projects/billit-mcp`: App Runner, ECR, private RDS Postgres, Secrets Manager, Route53/ACM, CloudWatch, VPC connector, and explicit public egress for Billit API
- defer webhooks, resources, prompts, AP/AR, mark-paid, credit notes, bulk, semantic search, cashflow, self-billing, admin UI, dynamic client registration, and raw API passthrough

Live local canary:
- keep default pytest/CI hermetic
- local-only sandbox canary writes sanitized evidence to `.local/billit-live-canary/<timestamp>/`
- support `legacy-api-key-readonly` and `hosted-oauth-readonly` with a pre-seeded sandbox Billit OAuth grant
- require `BILLIT_SANDBOX_PARTY_ID` or `BILLIT_PARTY_ID`
- read secrets from env/macOS Keychain, including `BILLIT_SANDBOX_API_KEY_K4K` for legacy mode
- no writes unless `BILLIT_LIVE_CANARY_ALLOW_WRITES=1`
- no automated Billit login; persist no tokens, API keys, raw customer/invoice payloads, files, or webhook bodies
- prove auth, accountInformation/company sync, one live collection response, explicit PartyID, reports, financial transactions, one shared service helper, hosted OAuth refresh, and read-only invoice.prepare

Final verification:
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy billit src tests
uv run lint-imports
uv run pytest -q --cov=billit --cov=src/billit_mcp --cov-report=term-missing --cov-report=xml
uv run diff-cover coverage.xml --compare-branch=origin/master --diff-range-notation=... --fail-under=80
uv build
bounded startup smoke for `uv run python -m billit_mcp`
bounded startup smoke for `uv run uvicorn billit_mcp.http_app:create_app --factory`
local hosted `/mcp` initialize/tools-list smoke
local read-only live sandbox canary with sanitized evidence

Do not perform repo transfer, public visibility changes, git history rewrite, production writes, or browser automation.
```
