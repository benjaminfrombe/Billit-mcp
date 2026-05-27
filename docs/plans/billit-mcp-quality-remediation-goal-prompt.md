---
title: "Billit MCP - Quality Remediation Goal Prompt"
updated: 2026-05-26
---

# Billit MCP Quality Remediation Goal Prompt

```text
/goal Implement the Billit MCP quality remediation and Motium-style CI migration in the current repo.

Read AGENTS.md, docs/index.md, docs/architecture.md, and billit-mcp-quality-remediation-plan.md first. Treat `python -m billit_mcp` as the canonical runtime; `server.py` and `billit/tools/` are the legacy FastAPI adapter.

Deliver one PR-sized change that:
- makes normal pytest hermetic and unable to hit Billit unless `--live` is explicitly passed
- fixes MCP client lifecycle leaks without breaking FastAPI request-scoped cleanup
- rewires packaged MCP composite tools away from local `/ai/...` Billit calls into shared local service helpers
- resolves and tests report and financial-transaction endpoint drift
- adds a local-only read-first live Billit canary that writes sanitized evidence under `.local/billit-live-canary/<timestamp>/`
- removes unsafe/unwanted tracked artifacts from HEAD and expands `.gitignore`/`.dockerignore`
- migrates Poetry to uv + Hatchling with committed `uv.lock`
- adds CI with Ruff format/check, mypy, import-linter, pytest coverage, diff-cover, uv build, and installed runtime smoke
- updates README/docs/AGENTS/tasks.md for the new commands and canary

The live canary must run only on the local machine, default to sandbox, read credentials from env or macOS Keychain service `BILLIT_SANDBOX_API_KEY_K4K`, require `BILLIT_PARTY_ID`, perform no writes unless `BILLIT_LIVE_CANARY_ALLOW_WRITES=1`, and persist no secrets or raw customer/invoice payloads. It must prove auth, at least one real live collection response, the chosen report endpoint form, financial transaction listing behavior, and one shared composite helper path.

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
local read-only live canary with sandbox credentials

Do not perform repo transfer, public visibility changes, or git history rewrite in this goal.
```
