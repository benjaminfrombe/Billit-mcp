"""Hosted MCP claims verification helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from mcp.server.auth.middleware.auth_context import get_access_token

from billit_mcp.services.hosted_errors import HostedToolError

if TYPE_CHECKING:
    from billit_mcp.auth.security import JWTService


@dataclass(frozen=True)
class HostedClaims:
    """Typed hosted MCP claims used by tool handlers."""

    actor_id: str
    client_id: str
    correlation_id: str
    raw: dict[str, Any]


class HostedClaimsVerifier:
    """Verify hosted MCP bearer tokens and expose typed claim fields."""

    def __init__(self, jwt_service: JWTService) -> None:
        self._jwt_service = jwt_service

    async def claims(self, required_scope: str = "billit:read") -> dict[str, Any]:
        """Return verified current MCP claims from the auth context."""

        access_token = get_access_token()
        if access_token is None:
            raise HostedToolError("unauthenticated", "Hosted tool requires an MCP bearer token")
        claims = self._jwt_service.decode(access_token.token)
        scopes = set(str(claims.get("scope", "")).split())
        if required_scope not in scopes:
            raise HostedToolError(
                "insufficient_scope",
                f"Missing required scope: {required_scope}",
                error_code="INSUFFICIENT_SCOPE",
            )
        return claims

    def typed_claims(self, claims: dict[str, Any]) -> HostedClaims:
        """Return typed claim fields required by hosted tools."""

        return HostedClaims(
            actor_id=str(claims["sub"]),
            client_id=str(claims["client_id"]),
            correlation_id=str(claims["jti"]),
            raw=claims,
        )
