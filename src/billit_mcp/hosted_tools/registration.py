"""Registration for curated hosted Billit MCP tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from billit_mcp.services.filters import compile_order_params, compile_party_params
from billit_mcp.services.hosted_runtime import (
    HostedToolError,
    HostedToolRuntime,
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

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
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

        return await runtime.execute_tool(
            tool_name="billit.connection_status",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
        )

    @mcp.tool(name="billit.list_companies")
    async def list_companies(environment: str = "sandbox") -> dict[str, Any]:
        """List companies authorized for the current Billit connection."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            from sqlalchemy import select

            from billit_mcp.persistence.models import BillitCompany

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

        return await runtime.execute_tool(
            tool_name="billit.list_companies",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
        )

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

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.search_orders",
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

        return await runtime.execute_tool(
            tool_name="billit.search_orders",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.get_order")
    async def get_order(environment: str, company_party_id: int, order_id: int) -> dict[str, Any]:
        """Get one Billit order by ID."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.get_order",
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                return await client.request("GET", f"/orders/{order_id}")
            finally:
                await client.close()

        return await runtime.execute_tool(
            tool_name="billit.get_order",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

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
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.resolve_party",
                environment=environment,
                company_party_id=company_party_id,
            )
            params = compile_party_params(
                role=role,
                name=name,
                vat_number=vat_number,
                email=email,
                external_provider_id=external_provider_id,
            )
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
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.lookup_peppol_receiver",
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                return await client.request("GET", f"/peppol/participantInformation/{identifier}")
            finally:
                await client.close()

        return await runtime.execute_tool(
            tool_name="billit.lookup_peppol_receiver",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

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

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
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

        return await runtime.execute_tool(
            tool_name="billit.invoice.prepare",
            required_scope="billit:read",
            operation_class="read",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

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

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            connection, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.invoice.create_draft",
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
            idempotency_id: str | None = None
            if idempotency_key:
                record = await runtime.record_idempotency_started(
                    connection_id=connection.connection_id,
                    company_party_id=company_party_id,
                    operation_type="invoice_create_draft",
                    idempotency_key=idempotency_key,
                    operation_hash=operation_hash,
                )
                idempotency_id = record.idempotency_id
                if record.status == "succeeded" and record.billit_resource_id:
                    return success(
                        {
                            "idempotent_replay": True,
                            "order_id": record.billit_resource_id,
                        }
                    )
                if record.status in {"conflict", "unknown_side_effect"}:
                    raise HostedToolError(
                        "idempotency_replay_blocked",
                        f"Prior operation state is {record.status}",
                    )
            headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
            try:
                response = await client.request("POST", "/orders", json=payload, headers=headers)
                order_id = _order_id_from_response(response.get("data"))
                if response.get("success") and order_id:
                    if idempotency_id:
                        await runtime.record_idempotency_outcome(
                            idempotency_id=idempotency_id,
                            status="succeeded",
                            billit_resource_type="order",
                            billit_resource_id=str(order_id),
                        )
                    detail = await client.request("GET", f"/orders/{order_id}")
                    return detail if detail.get("success") else response
                if idempotency_id:
                    await runtime.record_idempotency_outcome(
                        idempotency_id=idempotency_id,
                        status="failed",
                        billit_error_code=str(response.get("error_code") or "BILLIT_ERROR"),
                    )
                return response
            except Exception:
                if idempotency_id:
                    await runtime.record_idempotency_outcome(
                        idempotency_id=idempotency_id,
                        status="unknown_side_effect",
                        billit_error_code="BILLIT_REQUEST_EXCEPTION",
                    )
                raise
            finally:
                await client.close()

        return await runtime.execute_tool(
            tool_name="billit.invoice.create_draft",
            required_scope="billit:invoice.create",
            operation_class="write",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.prepare_send")
    async def invoice_prepare_send(
        environment: str,
        company_party_id: int,
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> dict[str, Any]:
        """Prepare a server-owned confirmation challenge before sending an invoice."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            connection, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.invoice.prepare_send",
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
            _raise_if_send_ineligible(summary)
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

        return await runtime.execute_tool(
            tool_name="billit.invoice.prepare_send",
            required_scope="billit:invoice.send",
            operation_class="external_send",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.confirm_send")
    async def invoice_confirm_send(
        environment: str,
        company_party_id: int,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> dict[str, Any]:
        """Consume a confirmation challenge and send the invoice."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            connection = await runtime.resolve_connection(
                actor_id=str(claims["sub"]), environment=environment
            )
            await runtime.validate_company(
                connection_id=connection.connection_id,
                environment=environment,
                company_party_id=company_party_id,
            )
            challenge = await runtime.get_pending_confirmation_challenge(
                challenge_id=challenge_id,
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                environment=environment,
                company_party_id=company_party_id,
                operation_type="invoice_send",
                resource_type="order",
                required_scope="billit:invoice.send",
            )
            order_id = str(challenge.resource_id)
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.invoice.confirm_send",
                environment=environment,
                company_party_id=company_party_id,
            )
            try:
                order = await client.request("GET", f"/orders/{order_id}")
                if not order.get("success"):
                    return order
                current_summary = build_send_summary(
                    order.get("data"),
                    company_party_id=company_party_id,
                    transport_type=str(challenge.summary_json["transport_type"]),
                    strict_transport=bool(challenge.summary_json["strict_transport"]),
                )
                _raise_if_send_ineligible(current_summary)
                current_hash = hash_payload(current_summary)
                if current_hash != challenge.operation_hash or current_hash != operation_hash:
                    raise HostedToolError(
                        "challenge_changed",
                        "Invoice state changed after the confirmation challenge was created",
                    )
                consumed = await runtime.consume_confirmation_challenge(
                    challenge_id=challenge_id,
                    confirmation_token=confirmation_token,
                    operation_hash=current_hash,
                    actor_id=str(claims["sub"]),
                    client_id=str(claims["client_id"]),
                    connection_id=connection.connection_id,
                    environment=environment,
                    company_party_id=company_party_id,
                    operation_type="invoice_send",
                    resource_type="order",
                    resource_id=order_id,
                    required_scope="billit:invoice.send",
                )
                headers = (
                    {"StrictTransportType": "true"}
                    if consumed.summary_json.get("strict_transport")
                    else None
                )
                return await client.request(
                    "POST",
                    "/orders/commands/send",
                    json={
                        "Transporttype": consumed.summary_json["transport_type"],
                        "OrderIDs": [int(order_id)],
                    },
                    headers=headers,
                )
            finally:
                await client.close()

        return await runtime.execute_tool(
            tool_name="billit.invoice.confirm_send",
            required_scope="billit:invoice.send",
            operation_class="external_send",
            handler=handler,
            environment=environment,
            company_party_id=company_party_id,
        )

    @mcp.tool(name="billit.invoice.get_delivery_status")
    async def invoice_get_delivery_status(
        environment: str,
        company_party_id: int,
        order_id: int,
    ) -> dict[str, Any]:
        """Return a concise fresh-read delivery status."""

        async def handler(claims: dict[str, Any]) -> dict[str, Any]:
            _, client = await runtime.billit_client(
                actor_id=str(claims["sub"]),
                client_id=str(claims["client_id"]),
                correlation_id=str(claims["jti"]),
                tool_name="billit.invoice.get_delivery_status",
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

        return await runtime.execute_tool(
            tool_name="billit.invoice.get_delivery_status",
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


def _order_id_from_response(data: Any) -> Any:
    if isinstance(data, dict):
        return data.get("OrderID") or data.get("ID")
    return data


def _raise_if_send_ineligible(summary: dict[str, Any]) -> None:
    if not summary.get("order_id"):
        raise HostedToolError("invoice_send_ineligible", "Order ID is missing from Billit order")
    if summary.get("is_sent"):
        raise HostedToolError("invoice_already_sent", "Invoice is already marked as sent")
