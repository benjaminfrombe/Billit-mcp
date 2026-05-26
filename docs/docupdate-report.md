---
title: "Billit MCP - Documentation Refresh Report"
updated: 2026-05-26
---

# Billit MCP Documentation Refresh Report

This report records the full repository documentation refresh performed after
treating existing project docs as deprecated. The audit used the current code
surface rather than historical claims in older Markdown files.

## Billit MCP Documentation Inventory After Refresh

Tracked Markdown is now split into:

- Root public docs: `README.md`, `AGENTS.md`, `AUTO-UPDATE.md`, and `tasks.md`.
- Current project docs: `docs/index.md`, `docs/architecture.md`,
  `docs/configuration.md`, `docs/mcp-tools.md`, `docs/fastapi-adapter.md`,
  `docs/operations.md`, `docs/development-testing.md`,
  `docs/billit-api-reference.md`, and this report.
- Upstream Billit references: focused files under `billit_docs_markdown/`.
- Test documentation: `tests/README.md`.

Removed stale or unsafe public docs:

- `CLAUDE.md` duplicated architecture material, contained local/private agent
  workflow instructions, and was not appropriate as public source of truth.
- `comprehensive_business_analysis.md` contained account-specific business
  analysis unrelated to the public MCP package.
- `docs/AUTO-UPDATE-IMPROVED.md` duplicated `AUTO-UPDATE.md`.
- `billit_docs_markdown/all_docs.md` duplicated the split Billit reference
  files and created a large chunk dilution risk.

## Billit MCP Code Coverage Against Docs

Documentation exists for every major code area:

- `src/billit_mcp/`: documented in `README.md`, `docs/architecture.md`, and
  `docs/mcp-tools.md`.
- `billit/client.py`: documented in `docs/architecture.md`,
  `docs/configuration.md`, and `docs/operations.md`.
- `billit/dependencies.py`: documented in `docs/architecture.md`.
- `billit/services/`: documented in `docs/architecture.md`,
  `docs/development-testing.md`, and `docs/mcp-tools.md`.
- `billit/smart_search.py`: documented in `docs/architecture.md` and
  `docs/mcp-tools.md`.
- `billit/tools/`: documented in `docs/fastapi-adapter.md`.
- `billit/models/`: documented as implementation support in
  `docs/development-testing.md` and through route/tool docs.
- `tests/`: documented in `tests/README.md` and
  `docs/development-testing.md`.
- `billit_docs_markdown/`: documented in `billit_docs_markdown/index.md` and
  `docs/billit-api-reference.md`.

## Billit MCP Staleness Findings Resolved

The old README claimed 66 MCP tools across 15 domains. Current code registers
44 MCP tools in the packaged server. The new docs use the actual registered
tool list and separately document the broader legacy FastAPI route table.

The old docs pointed at `markov-kernel/Billit-mcp`. Public docs now point at
`olivier-motium/Billit-mcp`.

The old docs presented FastAPI/Uvicorn as the primary runtime. Current docs
identify `python -m billit_mcp` as canonical and describe FastAPI as a legacy
adapter.

The old docs duplicated auto-update advice across two files. Current docs keep
one `AUTO-UPDATE.md`.

The old docs included private or account-specific operational material. Current
public docs exclude those details.

## Billit MCP QMD Retrieval Report

Frontmatter was added to maintained Markdown so QMD has unique, descriptive
titles and freshness metadata. The docs were split into focused files under
`docs/` to reduce multi-topic chunk dilution.

The largest duplication risk, `billit_docs_markdown/all_docs.md`, was removed.
The empty `billit_docs_markdown/index.md` was replaced with a prose-rich hub
that links to the most useful upstream references by task.

Generic root headings were replaced with self-descriptive headings such as
`Billit MCP Runtime Quickstart`, `Billit MCP Shared Client and Response
Envelope`, and `Billit MCP FastAPI Route Table`.

## Billit MCP Remaining Documentation Risks

Some upstream Billit reference pages are intentionally short because they mirror
single upstream topics such as HTTP status codes. They now have frontmatter, but
they may still produce weaker standalone embeddings than the project docs.

Packaged MCP composite tools now call shared local service helpers instead of
forwarding `/ai/...` paths through the Billit REST client. Keep
`docs/mcp-tools.md` synchronized if new composite helpers are added.

The package metadata in `pyproject.toml` should stay aligned with the public
GitHub owner. Documentation references and package URLs were updated as part of
this refresh.

## Billit MCP Validation Results

The final repository documentation set contains 67 non-ignored Markdown files.
Every maintained Markdown file has `title` and `updated` frontmatter, and local
Markdown links resolve.

Historical validation commands from the documentation refresh:

- `poetry install`
- `poetry run ruff check .`
- `poetry run pytest -q`
- `git diff --check`
- custom frontmatter and local Markdown link checks over tracked and untracked
  non-ignored Markdown files

Results:

- Ruff: pass.
- Pytest: 81 passed, 23 skipped.
- Whitespace check: pass.
- Markdown frontmatter: pass.
- Local Markdown links: pass.

## Billit MCP Priority Documentation Follow-Ups

1. Re-run this report after changing the MCP tool surface so `docs/mcp-tools.md`
   does not drift from `src/billit_mcp/server.py`.
2. Add examples for common order payloads only after sandbox payloads are
   sanitized and confirmed against Billit behavior.
3. Add an ADR if the legacy FastAPI adapter is removed, promoted, or split into
   a separate package.
