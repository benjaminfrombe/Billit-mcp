---
title: "Billit MCP - Quality Remediation and CI Migration Plan"
updated: 2026-05-26
---

# Billit MCP Quality Remediation and CI Migration Plan

## Summary

Implement the Billit MCP remediation as one PR with ordered internal phases.
Keep GitHub repo ownership transfer, public visibility changes, and history
rewriting out of scope.

The PR must:

- make normal tests hermetic and unable to hit Billit unless `--live` is used
- fix packaged MCP correctness around client lifecycle, composite tools, and
  endpoint drift
- add a local live-data canary with sanitized evidence output
- remove unsafe or irrelevant tracked artifacts from HEAD
- migrate from Poetry to uv and Hatchling
- add Motium-style CI/linter gates suitable for this smaller package
- update docs and `tasks.md` alongside behavior/tooling changes

The canonical runtime remains `python -m billit_mcp`. The root `server.py`
FastAPI app remains a legacy local adapter unless a separate plan changes that
status.

## Ordered Implementation

### 1. Baseline and Hermetic Tests

- Record the starting baseline with the current commands:
  - `poetry run ruff check .`
  - `poetry run pytest -q`
- Update pytest setup so normal tests provide fake Billit env values:
  - `BILLIT_API_KEY=test-api-key`
  - `BILLIT_BASE_URL=http://test.invalid`
  - `BILLIT_PARTY_ID=1`
  - `BILLIT_CONTEXT_PARTY_ID=`
  - `RATE_LIMIT_PER_MINUTE=100000`
- Add an autouse non-live guard that fails any unexpected
  `BillitAPIClient.request` call unless the test monkeypatches it or `--live`
  is explicitly passed.
- Keep `tests/test_live_integration.py` skipped unless `--live` is passed.
- Move or mark `tests/test_integration.py` so it cannot use local real
  credentials accidentally.
- Add one regression test proving a normal test run refuses unmocked live Billit
  access.

### 2. Runtime Correctness

- Fix packaged MCP client lifecycle without weakening FastAPI request-scoped
  cleanup.
- Use a small lifecycle helper compatible with the installed `mcp` version:
  reuse one MCP-process client where possible and close it during server
  shutdown if the API supports a lifespan hook.
- Extract shared composite behavior into a service module following the existing
  `billit/smart_search.py` adapter-neutral pattern.
- Rewire packaged MCP composite tools so they call local shared helpers instead
  of forwarding `/ai/...` paths to Billit.
- Keep the public response envelope stable:
  `{success, data, error, error_code}`.
- Resolve endpoint drift for reports and financial transactions by using
  upstream docs when explicit, otherwise sandbox probes from the live local
  canary. Pin the chosen endpoint names in unit tests for both MCP and FastAPI
  surfaces.
- Review file upload forwarding: ensure multipart requests do not inherit a
  global JSON `Content-Type` header that breaks uploads.

### 3. Local Live-Data Canary

Add a local-only read-first canary script, for example
`scripts/local/live_billit_canary.py`.

The canary must:

- run only from the local machine, never in CI by default
- use sandbox by default:
  `BILLIT_BASE_URL=https://api.sandbox.billit.be/v1`
- read credentials from environment variables, with an optional macOS Keychain
  fallback for `BILLIT_SANDBOX_API_KEY_K4K` when `BILLIT_API_KEY` is unset
- require `BILLIT_PARTY_ID` from `.env`, shell env, or a local-only Keychain
  hydration step
- perform only read operations unless `BILLIT_LIVE_CANARY_ALLOW_WRITES=1`
- call the same local package code paths the PR changed, especially
  `BillitAPIClient`, report endpoint selection, financial transaction listing,
  and shared composite helpers
- write sanitized evidence under `.local/billit-live-canary/<timestamp>/`
- never write API keys, customer names, emails, full invoice payloads, or raw
  live response bodies to git-tracked files

Required read-only probes:

- account/authentication probe
- at least two of parties, orders, products, financial transactions
- report endpoint probe for whichever `/report(s)` form the implementation
  chooses
- one composite helper probe using live data, with only counts and endpoint
  status persisted

The canary passes when:

- authentication succeeds
- at least one live Billit collection endpoint returns a real successful
  response from the selected environment
- endpoint drift decisions are reflected in the canary report
- the sanitized report contains command, timestamp, base URL environment,
  endpoint names, counts/statuses, and no secrets or raw customer data

Expected command shape after uv migration:

```bash
BILLIT_API_KEY="$(security find-generic-password -w -s BILLIT_SANDBOX_API_KEY_K4K)" \
BILLIT_BASE_URL=https://api.sandbox.billit.be/v1 \
BILLIT_PARTY_ID="$BILLIT_PARTY_ID" \
uv run python scripts/local/live_billit_canary.py --read-only
```

If sandbox contains no usable sample data, run the same canary against
production in read-only mode only after explicitly setting
`BILLIT_LIVE_CANARY_ENV=production` and confirming no write probes are enabled.

### 4. Cleanup and Secret Boundaries

- Remove `kids4kids_business_insights_dashboard.html` from tracked HEAD.
- Remove unsafe Claude tmux scripts from tracked HEAD.
- Keep `tasks.md` tracked because repo instructions require it, but update it
  with current TODO, DONE, and Learnings.
- Add ignore coverage for `.codex/`, `.claude/`, `.local/`, caches, coverage
  output, and generated test reports.
- Add `.dockerignore` excluding `.env`, local agent folders, virtualenvs,
  caches, coverage output, and live canary evidence.
- Do not commit `.env`, Keychain output, raw Billit responses, package tokens,
  or logs containing credentials.
- Note in the PR that deleting a tracked file from HEAD does not scrub public
  Git history; history rewriting is a separate repo-ops decision.

### 5. uv and Hatchling Migration

- Convert `pyproject.toml` from Poetry to PEP 621.
- Use Hatchling as the build backend.
- Explicitly include both packages:
  - `billit`
  - `src/billit_mcp`
- Preserve the installed console script:
  `billit-mcp = "billit_mcp:main"`.
- Add `.python-version` for Python 3.12 unless implementation proves the
  package intentionally supports a newer version.
- Track `uv.lock` and stop ignoring the committed lockfile.
- Remove `poetry.lock`.
- Do not pin `python-multipart==0.0.7`; resolve to a version compatible with
  the selected FastAPI version.
- Add dev dependencies for:
  - `pytest`
  - `pytest-asyncio`
  - `pytest-cov`
  - `pytest-randomly`
  - `respx`
  - `ruff`
  - `mypy`
  - `import-linter`
  - `diff-cover`
- Add `tool.uv.exclude-newer` with a date close to the migration date to keep
  resolution reproducible.
- Update Dockerfile, setup script, README, AGENTS checks, operations docs, and
  development docs from Poetry commands to uv commands.

### 6. Motium-Style CI and Linter Gates

- Add `.github/workflows/ci.yml`.
- Trigger on pull requests and pushes to the default branch.
- Use `astral-sh/setup-uv`, `uv sync --locked`, and a concurrency group that
  cancels stale in-progress CI for the same ref.
- Split jobs:
  - `lint`: format check, Ruff, mypy, import-linter
  - `test`: pytest with coverage and diff-cover
  - optional `package`: `uv build` plus installed runtime smoke
- Port the useful Motium Ruff shape:
  `E`, `W`, `F`, `I`, `N`, `UP`, `B`, `SIM`, `TCH`, `RUF`, ignoring `E501`.
- Configure mypy strict enough to matter, with narrow overrides only for
  external packages or MCP decorator behavior that cannot be typed cleanly.
- Add import-linter boundaries for this repo:
  - adapters may import shared services and client code
  - shared services may import the client and models
  - shared client must not import adapters
  - models must stay adapter-independent
- Use diff coverage against the merge base with diff-cover's supported flags:
  `--compare-branch=origin/master --diff-range-notation=...` unless the
  verified default branch is different.

### 7. Verification and Documentation

Final local verification must run:

```bash
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy billit src tests
uv run lint-imports
uv run pytest -q --cov=billit --cov=src/billit_mcp --cov-report=term-missing --cov-report=xml
uv run diff-cover coverage.xml --compare-branch=origin/master --diff-range-notation=... --fail-under=80
uv build
uv run python -m billit_mcp
```

For `python -m billit_mcp`, use a bounded startup smoke that proves import and
process startup without hanging the handoff.

Run the local live canary after all runtime and packaging changes:

```bash
BILLIT_API_KEY="$(security find-generic-password -w -s BILLIT_SANDBOX_API_KEY_K4K)" \
BILLIT_BASE_URL=https://api.sandbox.billit.be/v1 \
BILLIT_PARTY_ID="$BILLIT_PARTY_ID" \
uv run python scripts/local/live_billit_canary.py --read-only
```

Update docs nearest to the changed behavior:

- README and development docs for uv commands
- architecture docs for MCP lifecycle and shared composite services
- MCP tool docs for endpoint and composite-tool changes
- operations/config docs for the local canary and Keychain usage
- `tasks.md` with TODO, DONE, and Learnings

## Acceptance Criteria

- Normal tests pass without real Billit credentials.
- Normal tests cannot accidentally hit Billit.
- Live tests and live canary require explicit local credentials.
- Packaged MCP tools no longer forward local `/ai/...` paths to Billit.
- Client lifecycle does not leak `httpx.AsyncClient` instances in the packaged
  MCP runtime.
- Endpoint choices for reports and financial transactions are documented,
  tested, and reflected in canary output.
- `uv.lock` is committed, Poetry lock/config is removed, and uv/Hatch package
  build works.
- CI runs Ruff format check, Ruff lint, mypy, import-linter, pytest coverage,
  diff-cover, and package/runtime smoke.
- Local live-data canary produces sanitized evidence under `.local/` and that
  evidence is ignored by git.
- No secrets, `.env`, raw live data, or local agent artifacts are tracked.

## Out of Scope

- GitHub repository transfer to another account.
- Making the repository public.
- Squashing or rewriting Git history.
- Removing the legacy FastAPI adapter.
- Adding new Billit business features beyond the correctness and tooling work
  above.
