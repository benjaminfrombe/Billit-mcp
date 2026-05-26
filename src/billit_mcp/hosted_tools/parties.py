"""Hosted OAuth party and Peppol MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from billit_mcp.services.filters import compile_party_params
from billit_mcp.services.hosted_runtime import HostedToolRuntime, success

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_party_tools(mcp: FastMCP, runtime: HostedToolRuntime) -> None:
    """Register hosted party and Peppol tools."""

    @mcp.tool(name="billit.resolve_party")
    async def resolve_party(
        environment: str,
        company_party_id: int,
        role: str,
        name: str | None = None,
        vat_number: str | None = None,
        email: str | None = None,
        external_provider_id: str | None = None,
    ) -> dict[str, Any]:
        """Resolve a customer or supplier without guessing on ambiguity."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            params = compile_party_params(
                role=role,
                name=name,
                vat_number=vat_number,
                email=email,
                external_provider_id=external_provider_id,
            )
            async with runtime.authorized_billit_client(
                claims=typed,
                environment=environment,
                company_party_id=company_party_id,
                tool_name="billit.resolve_party",
            ) as (_, client):
                response = await client.request("GET", "/parties", params=params)
            items = _items(response.get("data"))
            if len(items) == 1:
                return success(
                    {
                        "resolution": "single_match",
                        "party": items[0],
                        "confidence": 1.0,
                        "safe_to_use": True,
                    }
                )
            if len(items) > 1:
                return success(
                    {
                        "resolution": "ambiguous",
                        "candidates": items,
                        "confidence": 0.0,
                        "safe_to_use": False,
                    }
                )
            return success(
                {
                    "resolution": "no_match",
                    "party": None,
                    "confidence": 0.0,
                    "safe_to_use": False,
                }
            )

        return await runtime.execute_tool(
            tool_name="billit.resolve_party",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.lookup_peppol_receiver")
    async def lookup_peppol_receiver(
        environment: str,
        company_party_id: int,
        identifier: str,
    ) -> dict[str, Any]:
        """Check whether a receiver identifier is visible on Peppol."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            typed = runtime.typed_claims(claims)
            async with runtime.authorized_billit_client(
                claims=typed,
                environment=environment,
                company_party_id=company_party_id,
                tool_name="billit.lookup_peppol_receiver",
            ) as (_, client):
                return await client.request(
                    "GET",
                    f"/peppol/participantInformation/{quote(identifier, safe='')}",
                )

        return await runtime.execute_tool(
            tool_name="billit.lookup_peppol_receiver",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )


def _items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        items = data.get("Items") or data.get("items") or data.get("value")
        return items if isinstance(items, list) else []
    return data if isinstance(data, list) else []
