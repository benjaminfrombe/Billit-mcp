---
title: "Billit MCP - Documentation Index"
updated: 2026-05-26
---

# Billit MCP Documentation Index

This is the current documentation entry point for the Billit MCP repository.
The docs are organized around the actual codebase: the packaged MCP stdio
server, the shared Billit API client, the legacy FastAPI adapter, and the test
suite. Older root-level plans and task logs should not be used as source of
truth.

## Billit MCP Start Here for New Contributors

Start with [Project Overview and Quickstart](../README.md), then read
[Architecture and Data Flow](architecture.md). Together they explain the
runtime split between the curated local API-key stdio server, the hosted OAuth
runtime, and the legacy FastAPI adapter. They also explain the shared response
envelope and the directories you will edit most often.

After that, read [Development and Testing](development-testing.md). It explains
the required Ruff and Pytest gates, how tests mock Billit API calls, and when
live tests are appropriate.

## Billit MCP Start Here for API Consumers

Read [Configuration Reference](configuration.md) before wiring credentials into
an MCP client. It describes the required local API-key variables, production
versus sandbox base URLs, local write/send gates, macOS Keychain usage, and
the exact variables the server loads at runtime.

Then read [MCP Tool Reference](mcp-tools.md). It lists each registered MCP tool,
what Billit endpoint or helper it uses, and the raw legacy tool names that no
longer exist in the stdio MCP surface.

For hosted connector work, use [Architecture and Data Flow](architecture.md)
as the entry point. Hosted mode is intentionally separate from local API-key
stdio mode and exposes only the curated OAuth-safe MVP tool set.

## Billit MCP Start Here for Operators

Read [Operations Runbook](operations.md) when deploying, rotating credentials,
publishing, or troubleshooting startup failures. It covers local execution,
Docker, PyPI packaging, public release checks, and what to do when Billit
returns a transport or authentication error.

Use [Auto Update Configuration](../AUTO-UPDATE.md) when an MCP client should
always fetch the newest PyPI package instead of relying on a local install.

## Billit MCP Implementation References

[FastAPI Adapter Routes](fastapi-adapter.md) documents the legacy HTTP route
surface in `billit/tools/`. The adapter is useful for local route testing and
Swagger inspection, but the packaged MCP client entrypoint is
`python -m billit_mcp`.

[Billit API Source Reference](billit-api-reference.md) explains how to use the
upstream Billit reference snapshots under `../billit_docs_markdown/`. Those
files preserve Billit-specific payload examples and terminology without
duplicating implementation guidance into project docs.

## Billit MCP Documentation Maintenance

[Documentation Refresh Report](docupdate-report.md) records the current
docupdate audit: inventory, deleted stale docs, QMD retrieval improvements,
known gaps, and follow-up priorities. Update it when documentation structure or
public runtime behavior changes.

All maintained Markdown files should include `title` and `updated`
frontmatter. Use self-descriptive headings so QMD and other search tools can
retrieve focused chunks without relying on parent headings.
