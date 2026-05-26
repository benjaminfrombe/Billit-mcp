---
title: "Billit MCP - Hosted OAuth Refactor Plan"
updated: 2026-05-26
---

# Billit MCP Hosted OAuth Refactor Plan

## Summary

Refactor Billit MCP from a local API-key stdio connector into a hosted,
OAuth-secured remote MCP service while preserving local `python -m billit_mcp`
behavior.

The first hosted release is intentionally narrow:

- hosted Streamable HTTP MCP at `/mcp`
- MCP-client OAuth for the hosted server
- separate Billit OAuth bridge for Billit REST API access
- encrypted Billit grants in Postgres
- explicit company authorization before every Billit request
- curated read tools plus the sales-invoice prepare/create/send lifecycle
- server-owned confirmation challenges before invoice sending
- redacted audit logs
- AWS deployment on Olivier infra
- local-only live-data canary with sanitized evidence

Defer webhooks, MCP resources, MCP prompts, AP/AR intelligence, mark-paid,
credit notes, bulk operations, semantic search, cashflow, product sync,
self-billing, admin UI, and dynamic client registration until this hosted OAuth
path is stable.

## Current Repo Facts

- `python -m billit_mcp` is the canonical packaged runtime.
- The current packaged server is stdio-first and registers tools in
  `src/billit_mcp/server.py`.
- The root `server.py` FastAPI app and `billit/tools/` are the legacy local HTTP
  adapter.
- The current Billit client uses env-derived `BILLIT_API_KEY`,
  `BILLIT_BASE_URL`, `BILLIT_PARTY_ID`, and optional
  `BILLIT_CONTEXT_PARTY_ID`.
- Current MCP tools are raw-ish endpoint wrappers and include high-risk actions
  such as order deletion, invoice sending, SSO token creation, webhook secret
  refresh, financial transaction mutation, file download, and Peppol
  registration/send.
- The current pinned MCP SDK version is too old for Streamable HTTP. The first
  implementation gate is proving the SDK upgrade and ASGI mount shape.
- Normal pytest must remain hermetic; live Billit access must stay opt-in only.

## Hard Boundaries

Hosted mode and local mode must be mechanically separated.

```text
Local/private mode:
  stdio runtime
  API-key auth from env/keychain/.env
  legacy/raw tools allowed only for local/private usage

Hosted mode:
  Streamable HTTP /mcp
  MCP OAuth access token required
  Billit OAuth grant required
  no API-key fallback
  curated intent tools only
```

The hosted Billit code path must never call `BillitSettings.from_env()` or read
`BILLIT_API_KEY` / `BILLIT_PARTY_ID`. Hosted startup should fail if a hosted
provider is configured with local API-key credentials.

The MCP access token is for the Billit MCP server only. It must never be sent to
Billit. Billit access and refresh tokens must never be returned to MCP clients.

## Target Runtime Layout

Use a runtime split under `src/billit_mcp/`:

```text
src/billit_mcp/
  __main__.py              # keeps python -m billit_mcp compatible
  stdio.py                 # local/private stdio runtime
  http_app.py              # hosted ASGI app factory
  registry.py              # app factory: mode="stdio" | "hosted"
  local_tools/             # legacy/raw local-only MCP tools
  hosted_tools/            # curated hosted MCP tools only
  auth/                    # MCP OAuth server + Billit OAuth bridge
  persistence/             # SQLAlchemy models, Alembic, repositories
  services/                # safe domain services
  policy/                  # scopes, company entitlement, confirmations
  audit/                   # redacted audit event writer
```

Keep root `server.py` and `billit/tools/*` as the legacy FastAPI adapter. Do not
turn the root FastAPI app into the public MCP host.

Keep import-linter contracts strict:

- `billit_mcp` must not import `billit.tools`
- `billit.tools` must not import `billit_mcp`
- `billit.client` remains adapter independent

## Hosted HTTP Endpoints

MVP endpoints:

```text
POST /mcp
GET /mcp
GET /.well-known/oauth-protected-resource
GET /.well-known/oauth-authorization-server
GET /oauth/authorize
POST /oauth/token
POST /oauth/revoke
GET /oauth/jwks.json
GET /billit/connect
GET /billit/callback
GET /healthz
GET /readyz
GET /privacy
GET /docs
```

Do not ship `/admin/connections` in MVP. Do not ship inbound Billit webhooks in
MVP unless explicitly re-scoped after the hosted OAuth path is green.

## OAuth Architecture

There are two independent OAuth systems.

```text
MCP client -> Billit MCP server:
  OAuth access token scoped to this MCP protected resource.

Billit MCP server -> Billit API:
  encrypted Billit OAuth grant stored server-side.
```

### MCP Client OAuth

MVP uses static registered OAuth clients. Before public connector launch, decide
and implement one of:

- pre-registered client IDs for each supported MCP client, or
- MCP Client ID Metadata Document support.

Do not implement Dynamic Client Registration in MVP.

Authorization server behavior:

- authorization-code flow only
- PKCE `S256` required
- exact redirect URI matching
- short-lived one-time auth codes
- access token audience bound to the `/mcp` protected resource
- token revocation endpoint
- JWKS endpoint if JWT access tokens are used

Access token claims if using JWT:

```text
iss
sub
aud
client_id
scope
jti
iat
nbf
exp
```

Failure behavior:

```text
missing token -> 401 with WWW-Authenticate
expired/wrong issuer/wrong audience/revoked -> 401 invalid_token
missing scope -> 403 insufficient_scope
disabled client -> 401 invalid_client
```

### Billit OAuth Bridge

Billit OAuth is separate from MCP OAuth.

`GET /billit/connect`:

- requires an active MCP authorization transaction or local hosted admin session
- selects `sandbox` or `production` explicitly
- creates signed state bound to the authorization transaction
- redirects to the Billit login URL with registered `client_id`,
  `redirect_uri`, and state

`GET /billit/callback`:

- validates state and TTL
- handles `error=access_denied`
- exchanges the authorization code once
- uses JSON body and no Authorization header for Billit token exchange
- stores encrypted access token, encrypted one-time refresh token, expiry, and
  refresh token hash
- syncs authorized companies from Billit account information
- resumes the MCP authorization transaction

Refresh behavior:

```text
SELECT grant row FOR UPDATE
if access token valid beyond skew, reuse it
else exchange refresh token
atomically replace access token, refresh token, expiry, hash, and version
on invalid/revoked refresh, mark connection reauthorization_required
never retry blindly after a one-time refresh-token failure
```

## Company Authorization

Every hosted tool input must include:

```text
environment
company_party_id
```

Every hosted Billit API request must send:

```text
Authorization: Bearer <Billit access token>
PartyID: <validated company_party_id>
```

Before any hosted Billit request, enforce:

```text
connection is active
environment matches the connection
company_party_id exists in billit_companies for that connection
company row is active
actor/client is allowed for that company
ContextPartyID is absent
```

Disable `ContextPartyID` in MVP. Add accountant context only after Billit
confirms how to derive and authorize it from account information or another
official endpoint.

## Persistence

Use Postgres, async SQLAlchemy, and Alembic.

Store runtime secrets in AWS Secrets Manager. Store sensitive database values
with app-level envelope encryption. Audit logs must not contain secrets, raw
invoice payloads, raw customer payloads, file contents, or webhook bodies.

### Required Tables

`actors`

- local user identity
- `actor_id` primary key
- stable subject hash
- optional encrypted display email
- disabled timestamp

`oauth_clients`

- static MCP OAuth clients
- exact redirect URI allowlist
- allowed scopes
- active/disabled status
- secret hash for confidential clients

`oauth_authorization_transactions`

- links `/oauth/authorize`, optional `/billit/connect`, `/billit/callback`, and
  final MCP code issuance
- client, actor, redirect URI, scope, state hash, environment, status, expiry

`oauth_auth_codes`

- code hash primary key
- client, actor, redirect URI, PKCE challenge, scopes, expiry, used timestamp
- one-time atomic consumption

`oauth_refresh_tokens`

- only if MCP clients receive refresh tokens
- token hash, token family, client, actor, scopes, expiry, rotated/revoked state
- rotate on every use

`oauth_token_revocations`

- revoked access token `jti` hashes and expiry

`billit_connections`

- actor plus Billit environment
- status: active, reauthorization_required, revoked, disabled
- timestamps for connect, refresh, revoke, reauth required

`billit_oauth_grants`

- one row per Billit connection
- encrypted access token
- encrypted refresh token
- refresh token hash
- access token expiry
- refresh token version
- encryption key version

`billit_companies`

- authorized companies from Billit account information
- primary key: connection, environment, company_party_id
- active flag and last seen timestamp
- hashed VAT/name metadata where needed

`confirmation_challenges`

- server-owned confirmation state
- actor, client, connection, environment, company_party_id
- operation type, resource ID, operation hash, redacted summary
- token hash, nonce hash, expiry, pending/consumed/expired/cancelled status

`idempotency_records`

- local duplicate-operation guard
- unique connection/company/operation/idempotency-key hash
- operation hash, status, Billit resource references, error code

`audit_events`

- append-only redacted audit log
- actor, client, connection, company, event type, operation class, tool name
- resource refs, request/response hashes, outcome, error code, latency,
  correlation ID

## Hosted Tool Surface

MVP hosted tools:

```text
billit.connection_status
billit.list_companies
billit.search_orders
billit.get_order
billit.resolve_party
billit.lookup_peppol_receiver
billit.invoice.prepare
billit.invoice.create_draft
billit.invoice.prepare_send
billit.invoice.confirm_send
billit.invoice.get_delivery_status
```

Rules:

- No arbitrary raw Billit endpoint passthrough.
- No arbitrary OData strings. Compile structured filters to allowlisted OData.
- No hosted create/update/delete/send tools outside the invoice workflow.
- `resolve_party` returns ambiguity instead of guessing.
- `invoice.prepare` is read-only and returns blockers, warnings, normalized
  invoice preview, customer resolution, Peppol/transport guidance, and next
  action.
- `invoice.create_draft` creates an order but never sends it.
- `invoice.prepare_send` validates the Billit order and creates a confirmation
  challenge.
- `invoice.confirm_send` consumes the challenge atomically and calls Billit send.
- `invoice.get_delivery_status` uses fresh Billit reads only in MVP. Do not
  claim webhook-backed truth until webhook ingestion ships.

Deferred tools and surfaces:

```text
file/PDF/UBL retrieval
payables/AP tools
AR aging and reminders
mark paid
credit notes
bulk execution
webhook receiver and management
Peppol registration
SSO token
products/catalog
MCP resources
MCP prompts
semantic search
cashflow forecasting
self-billing
admin UI
dynamic client registration
```

## Confirmation Contract

Consequential tools must be two-step and server-owned.

```text
prepare_*:
  validates the operation
  writes confirmation_challenges row
  returns challenge_id, operation_hash, human summary, expiry

confirm_*:
  requires challenge_id and confirmation token
  recomputes unchanged operation_hash
  atomically consumes pending challenge
  executes the Billit operation
```

Never accept a generic model-provided `confirmed: true`.

Invoice send confirmation summary must include:

- company name and PartyID
- order ID and invoice number
- customer name and VAT/identifier hash or display-safe value
- amount including VAT
- currency
- transport type
- strict transport flag
- whether fallback is allowed

## Idempotency

Implement local idempotency for invoice draft creation before relying on Billit
idempotency.

Billit documentation currently disagrees on header spelling:

- header reference: `Idempotent-Key`
- idempotency page: `Idempotency-Key`

Sandbox verification must prove:

- accepted header spelling
- whether `/orders` supports it
- whether `/orders/commands/send` supports it
- conflict response shape

Until verified, support a feature flag or adapter constant so only one canonical
header is used after the sandbox canary proves it.

## AWS Deployment

Implement deployment in `olivier-aws-infra/projects/billit-mcp`.

Default host:

```text
App Runner service from ECR image
private RDS Postgres
Secrets Manager secret containers
VPC connector to private subnets
security group from App Runner connector to RDS
NAT Gateway or documented egress path for public Billit API access
IAM least privilege for Secrets Manager and CloudWatch logs
Route53/ACM custom domain
CloudWatch logs and alarms
```

`/healthz`:

- process alive

`/readyz`:

- DB reachable
- migrations current
- secrets resolvable
- signing key available
- Billit OAuth client config present for enabled environments

If App Runner cannot support the final Streamable HTTP behavior, request
lifetimes, or networking constraints, switch to ECS/Fargate before public
launch.

## Local Live-Data Canary

The implementation must include a local-only live-data canary and keep it out of
default pytest and CI.

Canary modes:

```text
legacy-api-key-readonly:
  keeps the current local/private API-key canary working

hosted-oauth-readonly:
  validates the new hosted OAuth/service path using a pre-seeded sandbox Billit
  OAuth grant in local Postgres
```

Canary requirements:

- local machine only
- sandbox by default
- no browser automation
- no automated Billit login
- no CI/default pytest execution
- no writes unless `BILLIT_LIVE_CANARY_ALLOW_WRITES=1`
- requires explicit `BILLIT_PARTY_ID` or `BILLIT_SANDBOX_PARTY_ID`
- reads secrets from env or macOS Keychain
- writes sanitized evidence to `.local/billit-live-canary/<timestamp>/`
- persists no access tokens, refresh tokens, API keys, raw customer payloads,
  raw invoice payloads, file contents, or webhook bodies

Minimum live proof:

- environment and credential source classification without secret values
- Billit auth works
- at least one live collection response from sandbox
- `accountInformation` succeeds and company sync can identify the chosen
  PartyID
- all live reads send explicit PartyID
- report endpoint and financial transaction endpoint behavior remain pinned
- one shared service helper path works against live data
- hosted OAuth mode can refresh a pre-seeded sandbox grant without losing the
  one-time refresh token
- invoice prepare runs as a read-only preflight against live sandbox data or
  synthetic input without creating an order

Evidence files:

```text
summary.json
config.redacted.json
probes.json
service-helper-proof.json
oauth-refresh-proof.redacted.json
README.md
```

## Implementation Sequence

### PR 1 - Runtime Split and SDK Proof

- Pin a specific MCP SDK version that supports Streamable HTTP.
- Add hosted ASGI app factory.
- Move stdio startup to `stdio.py`.
- Preserve `python -m billit_mcp`.
- Add hosted registry with dummy/read-only tool.
- Add tests for `/mcp` initialize and hosted tool listing.
- Snapshot hosted tool list and prove raw tools are absent.

Merge gate:

```bash
uv run python -m billit_mcp   # bounded startup smoke
uv run uvicorn billit_mcp.http_app:create_app --factory
uv run pytest tests/test_mcp_http_transport.py
```

### PR 2 - Persistence and Crypto Foundation

- Add SQLAlchemy async engine and Alembic.
- Add hosted settings module.
- Add encryption service backed by Secrets Manager/KMS material.
- Add initial models and migrations.
- Add migration and encryption tests.
- Ensure hosted code cannot read local API-key env settings.

Merge gate:

```bash
alembic upgrade head on fresh local Postgres
alembic downgrade/upgrade for the migration under test
pytest for encryption, constraints, and repository behavior
```

### PR 3 - MCP OAuth Server

- Implement static clients.
- Implement authorization-code flow with PKCE S256.
- Add protected-resource metadata and authorization-server metadata.
- Add token endpoint, revocation, and JWKS if JWT is used.
- Add authorization transaction state table.

Merge gate:

- bad client, bad redirect, missing PKCE, wrong verifier, expired code, and code
  reuse are rejected
- wrong issuer/audience/revoked tokens are rejected at `/mcp`
- insufficient scope returns `403 insufficient_scope`

### PR 4 - Billit OAuth Bridge and Company Sync

- Add `/billit/connect` and `/billit/callback`.
- Exchange Billit code with JSON body and no Authorization header.
- Store encrypted grants.
- Implement row-locked refresh.
- Sync account/company information.
- Mark failed refresh as `reauthorization_required`.

Merge gate:

- state mismatch rejected
- sandbox and production credentials do not mix
- refresh concurrency causes only one refresh
- one-time refresh token rotation is atomic
- company sync populates authorized companies

### PR 5 - Hosted Read Tools

- Add connection/company/order/party/Peppol services.
- Add hosted tools for connection status, companies, order search/detail, party
  resolution, and Peppol lookup.
- Add safe OData compiler.
- Add redacted audit for read tools.

Merge gate:

- every hosted tool requires token and scope
- every Billit call includes explicit PartyID
- unauthorized company returns structured 403
- arbitrary OData is rejected
- hosted tool snapshot excludes raw local tools

### PR 6 - Invoice Prepare and Create Draft

- Add invoice input schema and normalization.
- Validate company, customer, dates, currency, VAT, and lines.
- Resolve customer with ambiguity handling.
- Add local idempotency records.
- Create draft order and fetch Billit-calculated totals.
- Verify Billit auto-send risk before production.

Merge gate:

- ambiguous party does not write
- invalid invoice returns blockers
- draft creation cannot send
- idempotent retry is safe
- audit contains summary and hashes only

### PR 7 - Confirmation-Gated Invoice Send

- Add `invoice.prepare_send`.
- Add `invoice.confirm_send`.
- Add confirmation challenge storage and atomic consumption.
- Call Billit send only after consuming a valid challenge.
- Map delivery status without conflating delivery with payment.

Merge gate:

- send without challenge fails
- expired challenge fails
- changed operation hash fails
- wrong actor/client/company fails
- challenge is single-use
- insufficient `billit:invoice.send` fails

### PR 8 - AWS Hosted Deployment

- Add `olivier-aws-infra/projects/billit-mcp`.
- Add App Runner/ECR/RDS/Secrets Manager/Route53/ACM/alarms.
- Add VPC connector, security groups, and public egress path for Billit API.
- Add deployment docs and migration runbook.

Merge gate:

- `/healthz` works
- `/readyz` validates DB/secrets/migrations/signing config
- RDS is private
- secrets are not in Terraform state
- App Runner can reach RDS and Billit API

### PR 9 - Canary, Docs, and Evals

- Extend local canary with hosted OAuth read-only mode.
- Add golden workflow evals for tool selection and safety boundaries.
- Update README, docs, tasks, privacy, setup, local mode, hosted mode, canary,
  and deployment docs.

Merge gate:

- local live sandbox canary produces sanitized evidence
- default pytest remains hermetic
- golden evals show zero unsafe writes before confirmation
- docs describe API-key mode as local/private/non-commercial only

## Test Matrix

Required final verification:

```bash
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy billit src tests
uv run lint-imports
uv run pytest -q --cov=billit --cov=src/billit_mcp --cov-report=term-missing --cov-report=xml
uv run diff-cover coverage.xml --compare-branch=origin/master --diff-range-notation=... --fail-under=80
uv build
```

Additional hosted checks:

```bash
uv run python -m billit_mcp
uv run uvicorn billit_mcp.http_app:create_app --factory
local hosted /mcp initialize smoke
local hosted tools/list snapshot
local read-only live canary with sandbox credentials
```

Blocking scenarios:

- stdio startup remains compatible
- hosted `/mcp` initialize works
- hosted raw tools absent
- OAuth bad client/redirect/PKCE/code/token/scope cases fail closed
- Billit OAuth state/code/refresh/environment cases fail closed
- hosted calls never use process API-key or process PartyID
- unauthorized company rejected
- structured filter compiler rejects arbitrary OData
- party ambiguity returns candidates without writing
- create draft cannot send
- send requires server-owned confirmation
- audit redacts tokens and raw payloads
- live canary writes only sanitized evidence

Golden workflow evals:

```text
create invoice for known customer
create invoice for ambiguous customer
create invoice with unauthorized company
create draft then send after confirmation
attempt send without confirmation
attempt send with stale amount
Peppol unavailable with strict transport
Peppol unavailable with fallback allowed
expired Billit refresh token
wrong environment PartyID
```

Target scores:

```text
unsafe_action_rate = 0
raw_tool_selected = 0
write_before_confirmation = 0
wrong_company_write = 0
ambiguous_party_autoselected = 0
```

## Billit Verification Gates

Resolve before production MVP:

- exact production redirect URI and approval process
- whether public launch needs Client ID Metadata Documents for target clients
- Billit token endpoint paths and error codes
- accountInformation user/company/role shape
- whether OAuth API calls require or accept PartyID exactly like API-key calls
- ContextPartyID/accountant authorization semantics
- whether `POST /orders` can be guaranteed draft/not-sent
- whether automatic sending can affect API-created orders
- `Idempotency-Key` versus `Idempotent-Key` spelling
- whether idempotency applies to `/orders` and `/orders/commands/send`
- send-already-sent behavior
- strict transport spelling and fallback behavior
- Billit rate limits by client, user, PartyID, and environment
- Peppol lookup identifier formats and sandbox/production behavior

## Out of Scope for MVP

- repository ownership transfer
- public visibility changes
- git history rewrite
- webhook receiver/status cache
- hosted admin UI
- dynamic client registration
- accountant `ContextPartyID` writes
- production write canaries
- automated Billit login
- arbitrary raw Billit API passthrough
- broad AP/AR/accounting copilot features
