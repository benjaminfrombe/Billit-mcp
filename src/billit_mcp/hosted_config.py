"""Hosted Billit MCP configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_SCOPES = [
    "billit:read",
    "billit:invoice.create",
    "billit:invoice.send",
]


@dataclass(frozen=True)
class OAuthClientConfig:
    """Static MCP OAuth client configuration."""

    client_id: str
    redirect_uris: tuple[str, ...]
    allowed_scopes: tuple[str, ...]
    client_secret: str | None = None


@dataclass(frozen=True)
class HostedSettings:
    """Environment-backed settings for hosted Billit MCP mode."""

    public_base_url: str
    issuer_url: str
    resource_url: str
    database_url: str
    jwt_private_key_pem: str | None
    token_encryption_key: str | None
    environment: str
    billit_sandbox_client_id: str | None
    billit_sandbox_client_secret: str | None
    billit_production_client_id: str | None
    billit_production_client_secret: str | None
    billit_sandbox_redirect_uri: str
    billit_production_redirect_uri: str
    static_clients: tuple[OAuthClientConfig, ...]

    @classmethod
    def from_env(cls) -> HostedSettings:
        """Build hosted settings without reading local Billit API-key variables."""

        public_base_url = os.getenv("BILLIT_MCP_PUBLIC_BASE_URL", "http://localhost:8000")
        issuer_url = os.getenv("BILLIT_MCP_ISSUER_URL", public_base_url)
        resource_url = os.getenv("BILLIT_MCP_RESOURCE_URL", f"{public_base_url.rstrip('/')}/mcp")
        database_url = os.getenv(
            "BILLIT_MCP_DATABASE_URL",
            "sqlite+aiosqlite:///.local/billit-mcp-hosted.db",
        )
        redirect_uri = f"{public_base_url.rstrip('/')}/billit/callback"
        return cls(
            public_base_url=public_base_url.rstrip("/"),
            issuer_url=issuer_url.rstrip("/"),
            resource_url=resource_url,
            database_url=database_url,
            jwt_private_key_pem=os.getenv("BILLIT_MCP_JWT_PRIVATE_KEY_PEM"),
            token_encryption_key=os.getenv("BILLIT_TOKEN_ENCRYPTION_KEY"),
            environment=os.getenv("BILLIT_MCP_ENVIRONMENT", "development"),
            billit_sandbox_client_id=os.getenv("BILLIT_OAUTH_CLIENT_ID_SANDBOX"),
            billit_sandbox_client_secret=os.getenv("BILLIT_OAUTH_CLIENT_SECRET_SANDBOX"),
            billit_production_client_id=os.getenv("BILLIT_OAUTH_CLIENT_ID_PRODUCTION"),
            billit_production_client_secret=os.getenv("BILLIT_OAUTH_CLIENT_SECRET_PRODUCTION"),
            billit_sandbox_redirect_uri=os.getenv(
                "BILLIT_OAUTH_REDIRECT_URI_SANDBOX", redirect_uri
            ),
            billit_production_redirect_uri=os.getenv(
                "BILLIT_OAUTH_REDIRECT_URI_PRODUCTION", redirect_uri
            ),
            static_clients=_static_clients_from_env(),
        )

    def billit_oauth_client(self, environment: str) -> tuple[str, str, str]:
        """Return Billit OAuth client settings for an environment."""

        if environment == "sandbox":
            client_id = self.billit_sandbox_client_id
            client_secret = self.billit_sandbox_client_secret
            redirect_uri = self.billit_sandbox_redirect_uri
        elif environment == "production":
            client_id = self.billit_production_client_id
            client_secret = self.billit_production_client_secret
            redirect_uri = self.billit_production_redirect_uri
        else:
            raise ValueError(f"Unsupported Billit environment: {environment}")
        if not client_id or not client_secret:
            raise RuntimeError(f"Billit OAuth client is not configured for {environment}")
        return client_id, client_secret, redirect_uri


def _static_clients_from_env() -> tuple[OAuthClientConfig, ...]:
    """Load a single static OAuth client from environment with a dev fallback."""

    client_id = os.getenv("BILLIT_MCP_OAUTH_CLIENT_ID", "local-dev-client")
    redirect_uris = tuple(
        uri.strip()
        for uri in os.getenv(
            "BILLIT_MCP_OAUTH_REDIRECT_URIS",
            "http://localhost:8765/callback,http://localhost/callback",
        ).split(",")
        if uri.strip()
    )
    scopes = tuple(
        scope.strip()
        for scope in os.getenv("BILLIT_MCP_OAUTH_SCOPES", " ".join(DEFAULT_SCOPES))
        .replace(",", " ")
        .split()
        if scope.strip()
    )
    secret = os.getenv("BILLIT_MCP_OAUTH_CLIENT_SECRET")
    return (OAuthClientConfig(client_id, redirect_uris, scopes, secret),)
