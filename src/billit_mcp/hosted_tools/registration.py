"""Registration for curated hosted Billit MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from billit_mcp.services.filters import compile_order_params
from billit_mcp.services.hosted_runtime import (
    HostedToolRuntime,
    error_result,
    hash_payload,
    success,
)
from billit_mcp.services.invoice import (
    build_invoice_payload,
    build_invoice_preflight,
    build_send_summary,
)

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP


def register_hosted_tools(mcp: FastMCP, runtime: HostedToolRuntime) -> None:
    """Register only the public hosted MVP tool surface."""

    @mcp.tool(name="billit.connection_status")
    async def connection_status(environment: str = "sandbox") -> dict[str, Any]:
        """Return the current hosted Billit connection status."""

        try:
            claims = await runtime.claims("billit:read")
            connection = await runtime.resolve_connection(
                actor_id=str(claims["sub"]), environment=environment
            )
            return success(
                {
                    "connected": True,
                    "environment": environment,
                    "token_status": connection.status,
                    "connection_id": connection.connection_id,
                }
            )
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.list_companies")
    async def list_companies(environment: str = "sandbox") -> dict[str, Any]:
        """List companies authorized for the current Billit connection."""

        try:
            from sqlalchemy import select

            from billit_mcp.persistence.models import BillitCompany

            claims = await runtime.claims("billit:read")
            connection = await runtime.resolve_connection(
                actor_id=str(claims["sub"]), environment=environment
            )
            async with runtime.database.session() as session:
                companies = (
                    await session.scalars(
                        select(BillitCompany).where(
                            BillitCompany.connection_id == connection.connection_id,
                            BillitCompany.environment == environment,
                            BillitCompany.active.is_(True),
                        )
                    )
                ).all()
                data = [
                    {
                        "company_party_id": company.company_party_id,
                        "environment": company.environment,
                        "active": company.active,
                        "is_default": company.is_default,
                    }
                    for company in companies
                ]
            return success({"companies": data})
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.search_orders")
    async def search_orders(
        environment: str,
        company_party_id: int,
        direction: str | None = None,
        order_type: str | None = None,
        customer_name: str | None = None,
        vat_number: str | None = None,
        paid: bool | None = None,
        modified_since: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search orders using structured allowlisted filters."""

        try:
            claims = await runtime.claims("billit:read")
            connection, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            params = compile_order_params(
                direction=direction,
                order_type=order_type,
                customer_name=customer_name,
                vat_number=vat_number,
                paid=paid,
                modified_since=modified_since,
                limit=limit,
            )
            try:
                return await client.request("GET", "/orders", params=params)
            finally:
                await client.close()
                await runtime.audit(
                    actor_id=str(claims["sub"]),
                    client_id=str(claims["client_id"]),
                    connection_id=connection.connection_id,
                    environment=environment,
                    company_party_id=company_party_id,
                    event_type="tool_call",
                    operation_class="read",
                    tool_name="billit.search_orders",
                    outcome="success",
                    correlation_id=str(claims["jti"]),
                )
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.get_order")
    async def get_order(environment: str, company_party_id: int, order_id: int) -> dict[str, Any]:
        """Get one Billit order by ID."""

        try:
            claims = await runtime.claims("billit:read")
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                return await client.request("GET", f"/orders/{order_id}")
            finally:
                await client.close()
        except Exception as exc:
            return error_result(exc)

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

        try:
            claims = await runtime.claims("billit:read")
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            filters: list[str] = [
                f"PartyType eq '{'Customer' if role == 'customer' else 'Supplier'}'"
            ]
            if external_provider_id:
                filters.append(f"ExternalProviderID eq '{_odata_escape(external_provider_id)}'")
            elif vat_number:
                filters.append(f"VATNumber eq '{_odata_escape(vat_number)}'")
            elif email:
                filters.append(f"Email eq '{_odata_escape(email)}'")
            elif name:
                filters.append(f"contains(Name,'{_odata_escape(name)}')")
            params = {"$filter": " and ".join(filters), "$top": 5}
            try:
                response = await client.request("GET", "/parties", params=params)
            finally:
                await client.close()
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
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.lookup_peppol_receiver")
    async def lookup_peppol_receiver(
        environment: str,
        company_party_id: int,
        identifier: str,
    ) -> dict[str, Any]:
        """Check whether a receiver identifier is visible on Peppol."""

        try:
            claims = await runtime.claims("billit:read")
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                return await client.request("GET", f"/peppol/participantInformation/{identifier}")
            finally:
                await client.close()
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.invoice.prepare")
    async def invoice_prepare(
        environment: str,
        company_party_id: int,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        desired_transport: str | None = None,
    ) -> dict[str, Any]:
        """Read-only invoice preflight."""

        try:
            claims = await runtime.claims("billit:read")
            connection = await runtime.resolve_connection(
                actor_id=str(claims["sub"]), environment=environment
            )
            await runtime.validate_company(
                connection_id=connection.connection_id,
                environment=environment,
                company_party_id=company_party_id,
            )
            return success(
                build_invoice_preflight(
                    customer=customer,
                    lines=lines,
                    order_date=order_date,
                    expiry_date=expiry_date,
                    desired_transport=desired_transport,
                )
            )
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.invoice.create_draft")
    async def invoice_create_draft(
        environment: str,
        company_party_id: int,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        external_provider_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a Billit sales invoice draft without sending it."""

        try:
            claims = await runtime.claims("billit:invoice.create")
            connection, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            payload = build_invoice_payload(
                customer=customer,
                lines=lines,
                order_date=order_date,
                expiry_date=expiry_date,
                external_provider_id=external_provider_id,
            )
            operation_hash = hash_payload(payload)
            if idempotency_key:
                await runtime.record_idempotency_started(
                    connection_id=connection.connection_id,
                    company_party_id=company_party_id,
                    operation_type="invoice_create_draft",
                    idempotency_key=idempotency_key,
                    operation_hash=operation_hash,
                )
            headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
            try:
                response = await client.request("POST", "/orders", json=payload, headers=headers)
                order_id = response.get("data")
                if isinstance(order_id, dict):
                    order_id = order_id.get("OrderID") or order_id.get("ID")
                if response.get("success") and order_id:
                    detail = await client.request("GET", f"/orders/{order_id}")
                    return detail if detail.get("success") else response
                return response
            finally:
                await client.close()
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.invoice.prepare_send")
    async def invoice_prepare_send(
        environment: str,
        company_party_id: int,
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> dict[str, Any]:
        """Prepare a server-owned confirmation challenge before sending an invoice."""

        try:
            claims = await runtime.claims("billit:invoice.send")
            connection, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                order = await client.request("GET", f"/orders/{order_id}")
            finally:
                await client.close()
            if not order.get("success"):
                return order
            summary = build_send_summary(
                order.get("data"),
                company_party_id=company_party_id,
                transport_type=transport_type,
                strict_transport=strict_transport,
            )
            challenge = await runtime.create_confirmation_challenge(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                connection_id=connection.connection_id,
                environment=environment,
                company_party_id=company_party_id,
                operation_type="invoice_send",
                resource_type="order",
                resource_id=str(order_id),
                required_scope="billit:invoice.send",
                summary=summary,
            )
            return success(challenge)
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.invoice.confirm_send")
    async def invoice_confirm_send(
        environment: str,
        company_party_id: int,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> dict[str, Any]:
        """Consume a confirmation challenge and send the invoice."""

        try:
            claims = await runtime.claims("billit:invoice.send")
            challenge = await runtime.consume_confirmation_challenge(
                challenge_id=challenge_id,
                confirmation_token=confirmation_token,
                operation_hash=operation_hash,
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
            )
            if (
                challenge.environment != environment
                or challenge.company_party_id != company_party_id
            ):
                return error_result(ValueError("Challenge company/environment mismatch"))
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            summary = challenge.summary_json
            headers = {"StrictTransportType": "true"} if summary.get("strict_transport") else None
            try:
                return await client.request(
                    "POST",
                    "/orders/commands/send",
                    json={
                        "Transporttype": summary["transport_type"],
                        "OrderIDs": [int(summary["order_id"])],
                    },
                    headers=headers,
                )
            finally:
                await client.close()
        except Exception as exc:
            return error_result(exc)

    @mcp.tool(name="billit.invoice.get_delivery_status")
    async def invoice_get_delivery_status(
        environment: str,
        company_party_id: int,
        order_id: int,
    ) -> dict[str, Any]:
        """Return a concise fresh-read delivery status."""

        try:
            claims = await runtime.claims("billit:read")
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                order = await client.request("GET", f"/orders/{order_id}")
            finally:
                await client.close()
            if not order.get("success"):
                return order
            data = order.get("data") or {}
            return success(
                {
                    "order_id": order_id,
                    "is_sent": bool(data.get("IsSent")),
                    "paid": bool(data.get("Paid")),
                    "delivery_status": data.get("DeliveryStatus")
                    or data.get("OrderStatus")
                    or "unknown",
                    "messages": data.get("Messages") or [],
                    "source": "fresh_billit_read",
                }
            )
        except Exception as exc:
            return error_result(exc)


def _items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        items = data.get("Items") or data.get("items") or data.get("value")
        return items if isinstance(items, list) else []
    return data if isinstance(data, list) else []


def _odata_escape(value: str) -> str:
    return value.replace("'", "''")
