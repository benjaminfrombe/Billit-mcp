"""Hosted ASGI app for Billit MCP."""

from __future__ import annotations

from contextlib import asynccontextmanager, suppress
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from billit_mcp.auth.billit_oauth import BillitOAuthBridge, new_billit_state
from billit_mcp.auth.oauth_service import MCPJWTVerifier, MCPOAuthService, OAuthError
from billit_mcp.auth.security import (
    FernetCipher,
    JWTService,
    ensure_aware_utc,
    random_token_urlsafe,
    sha256_text,
)
from billit_mcp.hosted_config import DEFAULT_SCOPES, HostedSettings
from billit_mcp.persistence.database import HostedDatabase
from billit_mcp.persistence.migrations import HOSTED_ALEMBIC_HEAD
from billit_mcp.persistence.models import OAuthAuthorizationTransaction
from billit_mcp.registry import create_hosted_mcp
from billit_mcp.services.hosted_runtime import HostedToolRuntime

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


def create_app() -> FastAPI:
    """Create the hosted Billit MCP ASGI application."""

    settings = HostedSettings.from_env()
    database = HostedDatabase(settings.database_url)
    jwt_service = JWTService(settings)
    cipher = FernetCipher.from_settings(settings)
    billit_bridge = BillitOAuthBridge(database, settings, cipher)
    oauth_service = MCPOAuthService(database, settings, jwt_service)
    verifier = MCPJWTVerifier(oauth_service)
    runtime = HostedToolRuntime(
        settings=settings,
        database=database,
        jwt_service=jwt_service,
        billit_bridge=billit_bridge,
    )
    mcp = create_hosted_mcp(runtime, verifier)
    streamable_app = mcp.streamable_http_app()
    startup_seed_error: str | None = None

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        nonlocal startup_seed_error
        try:
            revision = await database.alembic_revision()
            if revision == HOSTED_ALEMBIC_HEAD:
                await oauth_service.seed_static_clients()
            else:
                startup_seed_error = f"database revision is {revision!r}, expected head"
        except Exception as exc:  # readiness reports the concrete failure.
            startup_seed_error = str(exc)
        async with streamable_app.router.lifespan_context(streamable_app):
            yield
        await database.close()

    app = FastAPI(title="Billit MCP Hosted", lifespan=lifespan, docs_url=None, redoc_url=None)
    app.state.hosted_settings = settings
    app.state.hosted_database = database
    app.state.hosted_oauth_service = oauth_service
    app.state.hosted_billit_bridge = billit_bridge
    app.state.hosted_jwt_service = jwt_service
    app.state.hosted_mcp = mcp

    async def audit_auth(
        event_type: str,
        outcome: str,
        *,
        actor_id: str | None = None,
        client_id: str | None = None,
        environment: str | None = None,
        error_code: str | None = None,
        summary: dict[str, Any] | None = None,
    ) -> None:
        with suppress(Exception):
            await runtime.audit(
                actor_id=actor_id,
                client_id=client_id,
                event_type=event_type,
                operation_class="auth",
                outcome=outcome,
                correlation_id=random_token_urlsafe(),
                environment=environment,
                summary=summary,
                error_code=error_code,
            )

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/readyz")
    async def readyz() -> JSONResponse:
        configured_billit = {
            "sandbox": bool(
                settings.billit_sandbox_client_id and settings.billit_sandbox_client_secret
            ),
            "production": bool(
                settings.billit_production_client_id and settings.billit_production_client_secret
            ),
        }
        db_connected = False
        revision: str | None = None
        readiness_error: str | None = startup_seed_error
        try:
            await database.ping()
            db_connected = True
            revision = await database.alembic_revision()
        except Exception as exc:
            readiness_error = str(exc)
        ready = db_connected and revision == HOSTED_ALEMBIC_HEAD and startup_seed_error is None
        payload = {
            "status": "ok" if ready else "unready",
            "database": {
                "connected": db_connected,
                "alembic_revision": revision,
                "expected_revision": HOSTED_ALEMBIC_HEAD,
            },
            "resource": settings.resource_url,
            "issuer": settings.issuer_url,
            "billit_oauth": configured_billit,
            "error": readiness_error if not ready else None,
        }
        return JSONResponse(payload, status_code=200 if ready else 503)

    @app.get("/.well-known/oauth-protected-resource")
    async def protected_resource_metadata() -> dict[str, Any]:
        return {
            "resource": settings.resource_url,
            "authorization_servers": [settings.issuer_url],
            "scopes_supported": DEFAULT_SCOPES,
            "bearer_methods_supported": ["header"],
        }

    @app.get("/.well-known/oauth-authorization-server")
    async def authorization_server_metadata() -> dict[str, Any]:
        return {
            "issuer": settings.issuer_url,
            "authorization_endpoint": f"{settings.public_base_url}/oauth/authorize",
            "token_endpoint": f"{settings.public_base_url}/oauth/token",
            "revocation_endpoint": f"{settings.public_base_url}/oauth/revoke",
            "jwks_uri": f"{settings.public_base_url}/oauth/jwks.json",
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code"],
            "code_challenge_methods_supported": ["S256"],
            "scopes_supported": DEFAULT_SCOPES,
        }

    @app.get("/oauth/jwks.json")
    async def jwks() -> dict[str, Any]:
        return jwt_service.jwks()

    @app.get("/oauth/authorize")
    async def oauth_authorize(request: Request) -> Any:
        query = request.query_params
        try:
            if query.get("response_type") != "code":
                raise OAuthError("unsupported_response_type", "response_type must be code")
            actor_subject = query.get("login_hint") or "local-dev-actor"
            redirect_to = await oauth_service.authorize(
                client_id=_required(query.get("client_id"), "client_id"),
                redirect_uri=_required(query.get("redirect_uri"), "redirect_uri"),
                scope=query.get("scope", "billit:read"),
                state=query.get("state"),
                code_challenge=_required(query.get("code_challenge"), "code_challenge"),
                code_challenge_method=_required(
                    query.get("code_challenge_method"), "code_challenge_method"
                ),
                actor_subject=actor_subject,
                environment=query.get("environment", "sandbox"),
            )
            await audit_auth(
                "mcp_oauth_authorize",
                "success",
                client_id=query.get("client_id"),
                environment=query.get("environment", "sandbox"),
            )
            return RedirectResponse(redirect_to)
        except OAuthError as exc:
            await audit_auth(
                "mcp_oauth_authorize",
                "denied",
                client_id=query.get("client_id"),
                environment=query.get("environment", "sandbox"),
                error_code=exc.error,
            )
            return JSONResponse(
                {"error": exc.error, "error_description": exc.description},
                status_code=400,
            )

    @app.post("/oauth/token")
    async def oauth_token(request: Request) -> Any:
        data = await _request_data(request)
        try:
            if data.get("grant_type") != "authorization_code":
                raise OAuthError("unsupported_grant_type", "grant_type must be authorization_code")
            token = await oauth_service.exchange_code(
                client_id=_required(data.get("client_id"), "client_id"),
                client_secret=data.get("client_secret"),
                redirect_uri=_required(data.get("redirect_uri"), "redirect_uri"),
                code=_required(data.get("code"), "code"),
                code_verifier=_required(data.get("code_verifier"), "code_verifier"),
            )
            claims = jwt_service.decode(str(token["access_token"]))
            await audit_auth(
                "mcp_oauth_token",
                "success",
                actor_id=str(claims.get("sub")),
                client_id=str(claims.get("client_id")),
            )
            return JSONResponse(token)
        except OAuthError as exc:
            await audit_auth(
                "mcp_oauth_token",
                "denied",
                client_id=data.get("client_id"),
                error_code=exc.error,
            )
            return JSONResponse(
                {"error": exc.error, "error_description": exc.description},
                status_code=400 if exc.error != "invalid_client" else 401,
            )

    @app.post("/oauth/revoke")
    async def oauth_revoke(request: Request) -> Any:
        data = await _request_data(request)
        token = data.get("token")
        if token:
            await oauth_service.revoke_token(str(token))
            await audit_auth("mcp_oauth_revoke", "success")
        return JSONResponse({})

    @app.get("/billit/connect")
    async def billit_connect(
        environment: str = "sandbox",
        actor_subject: str = "local-dev-actor",
    ) -> Any:
        try:
            state = new_billit_state()
            actor_id = await oauth_service.actor_for_subject(actor_subject)
            async with database.session() as session:
                transaction = OAuthAuthorizationTransaction(
                    client_id=settings.static_clients[0].client_id,
                    actor_id=actor_id,
                    redirect_uri=settings.billit_sandbox_redirect_uri
                    if environment == "sandbox"
                    else settings.billit_production_redirect_uri,
                    scopes=["billit:read"],
                    state_hash=sha256_text(state),
                    environment=environment,
                    status="billit_connect_pending",
                    expires_at=datetime.now(UTC) + timedelta(minutes=10),
                )
                session.add(transaction)
            await audit_auth(
                "billit_oauth_connect",
                "success",
                actor_id=actor_id,
                environment=environment,
            )
            return RedirectResponse(
                billit_bridge.authorization_url(environment=environment, state=state)
            )
        except Exception as exc:
            await audit_auth(
                "billit_oauth_connect",
                "failure",
                environment=environment,
                error_code="BILLIT_CONNECT_FAILED",
            )
            return JSONResponse(
                {"error": "billit_connect_failed", "message": str(exc)}, status_code=400
            )

    @app.get("/billit/callback")
    async def billit_callback(
        code: str | None = None,
        state: str | None = None,
        error: str | None = None,
    ) -> Any:
        if error:
            await audit_auth("billit_oauth_callback", "denied", error_code=str(error))
            return JSONResponse({"status": "access_denied", "error": error}, status_code=400)
        if not code or not state:
            return JSONResponse({"error": "missing_code_or_state"}, status_code=400)
        async with database.session() as session:
            from sqlalchemy import select

            transaction = await session.scalar(
                select(OAuthAuthorizationTransaction).where(
                    OAuthAuthorizationTransaction.state_hash == sha256_text(state),
                    OAuthAuthorizationTransaction.status == "billit_connect_pending",
                )
            )
            if transaction is None or transaction.actor_id is None:
                await audit_auth("billit_oauth_callback", "denied", error_code="invalid_state")
                return JSONResponse({"error": "invalid_state"}, status_code=400)
            if ensure_aware_utc(transaction.expires_at) <= datetime.now(UTC):
                await audit_auth("billit_oauth_callback", "denied", error_code="expired_state")
                return JSONResponse({"error": "expired_state"}, status_code=400)
            actor_id = transaction.actor_id
            environment = transaction.environment
            transaction.status = "billit_callback_received"
        try:
            connection_id = await billit_bridge.exchange_callback(
                actor_id=actor_id,
                environment=environment,
                code=code,
            )
            await audit_auth(
                "billit_oauth_callback",
                "success",
                actor_id=actor_id,
                environment=environment,
            )
            return JSONResponse({"status": "connected", "connection_id": connection_id})
        except Exception as exc:
            await audit_auth(
                "billit_oauth_callback",
                "failure",
                actor_id=actor_id,
                environment=environment,
                error_code="BILLIT_TOKEN_EXCHANGE_FAILED",
            )
            return JSONResponse(
                {"error": "billit_token_exchange_failed", "message": str(exc)}, status_code=400
            )

    @app.get("/privacy")
    async def privacy() -> Any:
        return HTMLResponse(
            "<h1>Billit MCP Privacy</h1><p>Hosted mode stores encrypted Billit OAuth "
            "grants, authorized company IDs, confirmation state, and redacted audit "
            "events. Tokens, raw invoice payloads, raw customer payloads, and file "
            "contents are not stored in audit logs.</p>"
        )

    @app.get("/docs")
    async def hosted_docs() -> Any:
        return HTMLResponse(
            "<h1>Billit MCP Hosted</h1><p>Use /mcp with an MCP OAuth bearer token. "
            "Local API-key mode remains limited to stdio/private usage.</p>"
        )

    app.mount("/", streamable_app)
    return app


async def _request_data(request: Request) -> dict[str, Any]:
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        payload = await request.json()
        return dict(payload)
    form = await request.form()
    return {key: str(value) for key, value in form.items()}


def _required(value: str | None, name: str) -> str:
    if not value:
        raise OAuthError("invalid_request", f"{name} is required")
    return value
