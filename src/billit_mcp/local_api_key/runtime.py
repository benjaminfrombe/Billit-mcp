"""Local/private API-key runtime services for curated stdio MCP tools."""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import uuid
from contextlib import suppress
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from time import perf_counter
from typing import Any, Protocol, cast
from urllib.parse import quote, urlparse

from billit.client import BillitAPIClient, BillitSettings
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit.services.ai_composite import generate_invoice_summary
from billit_mcp.local_api_key.state import (
    LocalConfirmationChallenge,
    LocalIdempotencyRecord,
    LocalStateStore,
)
from billit_mcp.services.filters import compile_order_params, compile_party_params
from billit_mcp.services.invoice import (
    build_invoice_payload,
    build_invoice_preflight,
    build_send_summary,
)

LOCAL_API_KEY_TOOL_NAMES = {
    "billit.connection_status",
    "billit.list_companies",
    "billit.search_orders",
    "billit.get_order",
    "billit.resolve_party",
    "billit.lookup_peppol_receiver",
    "billit.list_financial_transactions",
    "billit.list_reports",
    "billit.get_report",
    "billit.invoice.prepare",
    "billit.invoice.create_draft",
    "billit.invoice.prepare_send",
    "billit.invoice.confirm_send",
    "billit.invoice.get_delivery_status",
    "billit.invoice.summary",
}

SECURITY_DENIALS = {
    "configuration_error",
    "local_writes_disabled",
    "local_sends_disabled",
    "company_entitlement_unverified",
    "unauthorized_company",
    "context_party_id_disabled",
    "challenge_not_found",
    "challenge_expired",
    "challenge_mismatch",
    "challenge_token_invalid",
    "challenge_changed",
    "idempotency_conflict",
}


class LocalBillitClient(Protocol):
    """Minimal client protocol used by the local API-key runtime."""

    client: Any

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        """Perform a Billit request."""
        ...

    async def close(self) -> None:
        """Close the client."""
        ...


class LocalToolError(RuntimeError):
    """Structured local API-key tool error."""

    def __init__(
        self,
        error_type: str,
        message: str,
        *,
        severity: str = "blocking",
        retryable: bool = False,
        user_action_required: bool = True,
        error_code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
        self.severity = severity
        self.retryable = retryable
        self.user_action_required = user_action_required
        self.error_code = error_code or error_type.upper()

    def to_result(self) -> dict[str, Any]:
        """Return the stable Billit MCP envelope."""

        return failure(
            {
                "type": self.error_type,
                "severity": self.severity,
                "retryable": self.retryable,
                "user_action_required": self.user_action_required,
                "message": self.message,
            },
            self.error_code,
        )


@dataclass(frozen=True)
class CompanyStatus:
    """Parsed accountInformation entitlement state for the configured PartyID."""

    account_response: dict[str, Any]
    configured_party_id: str
    companies: list[dict[str, Any]]
    company_ids: set[str]
    parseable: bool
    authorized: bool
    warnings: list[str]

    @property
    def state(self) -> str:
        if self.authorized:
            return "verified"
        if self.company_ids:
            return "unauthorized"
        if self.parseable:
            return "inconclusive"
        return "inconclusive"


class LocalAPIKeyRuntime:
    """Runtime shared by the local/private API-key MCP tools."""

    def __init__(
        self,
        *,
        settings: BillitSettings | None = None,
        state: LocalStateStore | None = None,
        client_factory: Any = BillitAPIClient,
    ) -> None:
        self._settings = _local_settings(settings) if settings is not None else None
        self.state = state or LocalStateStore(
            os.getenv("BILLIT_MCP_LOCAL_STATE_DB", ".local/billit-mcp-api-key-state.db")
        )
        self.client_factory = client_factory
        self._client: LocalBillitClient | None = None

    async def get_client(self) -> LocalBillitClient:
        """Return the process-scoped explicit API-key Billit client."""

        if self._client is None or _client_is_closed(self._client):
            self._client = self.client_factory(self.settings())
        return self._client

    async def close(self) -> None:
        """Close the cached Billit client."""

        if self._client is not None:
            await self._client.close()
            self._client = None

    def settings(self) -> BillitSettings:
        """Return explicit local API-key settings with ContextPartyID disabled."""

        if self._settings is not None:
            return self._settings
        missing = missing_local_settings()
        if missing:
            raise LocalToolError(
                "configuration_error",
                "Missing required local API-key settings: " + ", ".join(missing),
                error_code="CONFIGURATION_ERROR",
            )
        rate_limit = os.getenv("RATE_LIMIT_PER_MINUTE")
        self._settings = BillitSettings(
            base_url=str(os.environ["BILLIT_BASE_URL"]),
            api_key=str(os.environ["BILLIT_API_KEY"]),
            party_id=str(os.environ["BILLIT_PARTY_ID"]),
            context_party_id=None,
            rate_limit_per_minute=int(rate_limit) if rate_limit else None,
        )
        return self._settings

    async def execute_tool(
        self,
        *,
        tool_name: str,
        operation_class: str,
        handler: Any,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> dict[str, Any]:
        """Run a local tool with centralized structured errors and audit."""

        started = perf_counter()
        outcome = "success"
        error_code: str | None = None
        correlation_id = _token()
        try:
            result = cast("dict[str, Any]", await handler())
            if not result.get("success", False):
                outcome = "failure"
                error_code = str(result.get("error_code") or "LOCAL_TOOL_FAILURE")
            return result
        except Exception as exc:
            result = error_result(exc)
            if isinstance(exc, LocalToolError) and exc.error_type in SECURITY_DENIALS:
                outcome = "denied"
            else:
                outcome = "failure"
            error_code = str(result.get("error_code") or "LOCAL_TOOL_ERROR")
            return result
        finally:
            with suppress(Exception):
                await self.audit(
                    event_type="tool_call",
                    operation_class=operation_class,
                    outcome=outcome,
                    correlation_id=correlation_id,
                    tool_name=tool_name,
                    company_party_id=company_party_id,
                    resource_type=resource_type,
                    resource_id=resource_id,
                    error_code=error_code,
                    latency_ms=int((perf_counter() - started) * 1000),
                )

    async def audited_client(self, *, tool_name: str) -> LocalAuditedBillitClient:
        """Return a redacted-audit wrapper around the shared API-key client."""

        return LocalAuditedBillitClient(
            client=await self.get_client(),
            runtime=self,
            tool_name=tool_name,
            environment=environment_name(self.settings().base_url),
            company_party_id=self._configured_party_id_or_none(),
        )

    @property
    def configured_party_id(self) -> int:
        """Return the configured Billit PartyID as an integer."""

        try:
            return int(self.settings().party_id)
        except (TypeError, ValueError) as exc:
            raise LocalToolError(
                "configuration_error",
                "BILLIT_PARTY_ID must be an explicit numeric Billit PartyID",
                error_code="CONFIGURATION_ERROR",
            ) from exc

    async def connection_status(self) -> dict[str, Any]:
        """Check local API-key configuration, auth, and company entitlement."""

        async def handler() -> dict[str, Any]:
            missing = missing_local_settings()
            if missing:
                return success(
                    {
                        "connected": False,
                        "configuration_complete": False,
                        "missing_settings": missing,
                        "environment": environment_name(os.getenv("BILLIT_BASE_URL", "")),
                        "base_url_host": base_url_host(os.getenv("BILLIT_BASE_URL", "")),
                        "configured_party_id": os.getenv("BILLIT_PARTY_ID"),
                        "company_authorization": "not_checked",
                        "company_count": 0,
                        "writes_enabled": self.local_writes_enabled,
                        "sends_enabled": self.local_sends_enabled,
                        "context_party_id_enabled": False,
                        "warnings": [
                            "Missing required local API-key settings: " + ", ".join(missing)
                        ],
                        "state_path": str(self.state.path),
                    }
                )
            company = await self.company_status(tool_name="billit.connection_status")
            if not company.account_response.get("success"):
                return company.account_response
            settings = self.settings()
            return success(
                {
                    "connected": True,
                    "configuration_complete": True,
                    "environment": environment_name(settings.base_url),
                    "base_url_host": base_url_host(settings.base_url),
                    "configured_party_id": company.configured_party_id,
                    "company_authorization": company.state,
                    "company_count": len(company.companies),
                    "writes_enabled": self.local_writes_enabled,
                    "sends_enabled": self.local_sends_enabled,
                    "context_party_id_enabled": False,
                    "warnings": self.local_warnings() + company.warnings,
                    "state_path": str(self.state.path),
                }
            )

        return await self.execute_tool(
            tool_name="billit.connection_status",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def list_companies(self) -> dict[str, Any]:
        """List companies from accountInformation without storing raw payloads."""

        async def handler() -> dict[str, Any]:
            company = await self.company_status(tool_name="billit.list_companies")
            if not company.account_response.get("success"):
                return company.account_response
            return success(
                {
                    "configured_party_id": company.configured_party_id,
                    "company_authorization": company.state,
                    "companies": company.companies,
                    "warnings": self.local_warnings() + company.warnings,
                }
            )

        return await self.execute_tool(
            tool_name="billit.list_companies",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def search_orders(
        self,
        *,
        direction: str | None = None,
        order_type: str | None = None,
        customer_name: str | None = None,
        vat_number: str | None = None,
        paid: bool | None = None,
        modified_since: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Search orders using structured allowlisted filters only."""

        async def handler() -> dict[str, Any]:
            params = compile_order_params(
                direction=direction,
                order_type=order_type,
                customer_name=customer_name,
                vat_number=vat_number,
                paid=paid,
                modified_since=modified_since,
                limit=limit,
            )
            client = await self.audited_client(tool_name="billit.search_orders")
            return await client.request("GET", "/orders", params=params)

        return await self.execute_tool(
            tool_name="billit.search_orders",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def get_order(self, *, order_id: int) -> dict[str, Any]:
        """Get one Billit order by ID."""

        async def handler() -> dict[str, Any]:
            client = await self.audited_client(tool_name="billit.get_order")
            return await client.request("GET", f"/orders/{order_id}")

        return await self.execute_tool(
            tool_name="billit.get_order",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
            resource_type="order",
            resource_id=str(order_id),
        )

    async def resolve_party(
        self,
        *,
        role: str,
        name: str | None = None,
        vat_number: str | None = None,
        email: str | None = None,
        external_provider_id: str | None = None,
    ) -> dict[str, Any]:
        """Resolve a customer or supplier without guessing on ambiguity."""

        async def handler() -> dict[str, Any]:
            params = compile_party_params(
                role=role.lower(),
                name=name,
                vat_number=vat_number,
                email=email,
                external_provider_id=external_provider_id,
            )
            client = await self.audited_client(tool_name="billit.resolve_party")
            response = await client.request("GET", "/parties", params=params)
            if not response.get("success"):
                return response
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

        return await self.execute_tool(
            tool_name="billit.resolve_party",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def lookup_peppol_receiver(self, *, identifier: str) -> dict[str, Any]:
        """Check whether a receiver identifier is visible on Peppol."""

        async def handler() -> dict[str, Any]:
            client = await self.audited_client(tool_name="billit.lookup_peppol_receiver")
            return await client.request(
                "GET",
                f"/peppol/participantInformation/{quote(identifier, safe='')}",
            )

        return await self.execute_tool(
            tool_name="billit.lookup_peppol_receiver",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def list_financial_transactions(self, *, limit: int = 20) -> dict[str, Any]:
        """List financial transactions without raw OData passthrough."""

        async def handler() -> dict[str, Any]:
            client = await self.audited_client(tool_name="billit.list_financial_transactions")
            return await client.request(
                "GET",
                FINANCIAL_TRANSACTIONS_ENDPOINT,
                params=list_params(skip=0, top=limit),
            )

        return await self.execute_tool(
            tool_name="billit.list_financial_transactions",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def list_reports(self) -> dict[str, Any]:
        """List available reports."""

        async def handler() -> dict[str, Any]:
            client = await self.audited_client(tool_name="billit.list_reports")
            return await client.request("GET", report_endpoint())

        return await self.execute_tool(
            tool_name="billit.list_reports",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def get_report(
        self,
        *,
        report_id: str,
        parameters: dict[str, str | int | float | bool] | None = None,
    ) -> dict[str, Any]:
        """Get a report with bounded scalar parameters."""

        async def handler() -> dict[str, Any]:
            _validate_report_request(report_id, parameters or {})
            client = await self.audited_client(tool_name="billit.get_report")
            return await client.request(
                "GET",
                report_endpoint(report_id),
                params=parameters or {},
            )

        return await self.execute_tool(
            tool_name="billit.get_report",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
            resource_type="report",
            resource_id=report_id,
        )

    async def invoice_prepare(
        self,
        *,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        desired_transport: str | None = None,
    ) -> dict[str, Any]:
        """Run a read-only invoice preflight."""

        async def handler() -> dict[str, Any]:
            preflight = build_invoice_preflight(
                customer=customer,
                lines=lines,
                order_date=order_date,
                expiry_date=expiry_date,
                desired_transport=desired_transport,
            )
            preflight["company_party_id"] = self.settings().party_id
            preflight["writes_enabled"] = self.local_writes_enabled
            preflight["warnings"] = list(preflight.get("warnings") or []) + self.local_warnings()
            return success(preflight)

        return await self.execute_tool(
            tool_name="billit.invoice.prepare",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def invoice_create_draft(
        self,
        *,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        external_provider_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Create a Billit sales invoice draft without sending it."""

        async def handler() -> dict[str, Any]:
            self.require_writes_enabled()
            await self.validate_company_for_write(tool_name="billit.invoice.create_draft")
            preflight = build_invoice_preflight(
                customer=customer,
                lines=lines,
                order_date=order_date,
                expiry_date=expiry_date,
            )
            if preflight["blockers"]:
                raise LocalToolError(
                    "invoice_preflight_blocked",
                    "Invoice draft request has blocking validation issues",
                    error_code="INVOICE_PREFLIGHT_BLOCKED",
                )
            payload = build_invoice_payload(
                customer=customer,
                lines=lines,
                order_date=order_date,
                expiry_date=expiry_date,
                external_provider_id=external_provider_id,
            )
            operation_hash = hash_payload(payload)
            record = self._record_idempotency_started(
                operation_type="invoice_create_draft",
                idempotency_key=idempotency_key,
                operation_hash=operation_hash,
            )
            if record is not None:
                if record.operation_hash != operation_hash:
                    raise LocalToolError(
                        "idempotency_conflict",
                        "Idempotency key was already used for a different invoice draft",
                        error_code="IDEMPOTENCY_CONFLICT",
                    )
                if record.status == "succeeded" and record.billit_resource_id:
                    return success(
                        {
                            "idempotent_replay": True,
                            "order_id": record.billit_resource_id,
                        }
                    )
                if record.status in {"conflict", "unknown_side_effect"}:
                    raise LocalToolError(
                        "idempotency_replay_blocked",
                        f"Prior idempotent draft outcome is {record.status}",
                    )
            client = await self.audited_client(tool_name="billit.invoice.create_draft")
            headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
            try:
                response = await client.request("POST", "/orders", json=payload, headers=headers)
                order_id = _order_id_from_response(response.get("data"))
                if response.get("success") and order_id:
                    if record is not None:
                        self.state.record_idempotency_outcome(
                            idempotency_id=record.idempotency_id,
                            status="succeeded",
                            billit_resource_type="order",
                            billit_resource_id=str(order_id),
                        )
                    detail = await client.request("GET", f"/orders/{order_id}")
                    return detail if detail.get("success") else response
                if record is not None:
                    self.state.record_idempotency_outcome(
                        idempotency_id=record.idempotency_id,
                        status="failed",
                        billit_error_code=str(response.get("error_code") or "BILLIT_ERROR"),
                    )
                return response
            except Exception:
                if record is not None:
                    self.state.record_idempotency_outcome(
                        idempotency_id=record.idempotency_id,
                        status="unknown_side_effect",
                        billit_error_code="BILLIT_REQUEST_EXCEPTION",
                    )
                raise

        return await self.execute_tool(
            tool_name="billit.invoice.create_draft",
            operation_class="write",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def invoice_prepare_send(
        self,
        *,
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> dict[str, Any]:
        """Prepare a local confirmation challenge before sending an invoice."""

        async def handler() -> dict[str, Any]:
            self.require_sends_enabled()
            await self.validate_company_for_write(tool_name="billit.invoice.prepare_send")
            client = await self.audited_client(tool_name="billit.invoice.prepare_send")
            order = await client.request("GET", f"/orders/{order_id}")
            if not order.get("success"):
                return order
            summary = redacted_send_summary(
                order.get("data"),
                company_party_id=self.configured_party_id,
                transport_type=_transport_type(transport_type),
                strict_transport=strict_transport,
            )
            _raise_if_send_ineligible(summary)
            challenge = self.create_confirmation_challenge(
                operation_type="invoice_send",
                resource_type="order",
                resource_id=str(order_id),
                summary=summary,
            )
            return success(challenge)

        return await self.execute_tool(
            tool_name="billit.invoice.prepare_send",
            operation_class="external_send",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
            resource_type="order",
            resource_id=str(order_id),
        )

    async def invoice_confirm_send(
        self,
        *,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> dict[str, Any]:
        """Consume a confirmation challenge and send the invoice."""

        async def handler() -> dict[str, Any]:
            self.require_sends_enabled()
            await self.validate_company_for_write(tool_name="billit.invoice.confirm_send")
            challenge = self.get_pending_confirmation_challenge(challenge_id)
            order_id = challenge.resource_id
            client = await self.audited_client(tool_name="billit.invoice.confirm_send")
            order = await client.request("GET", f"/orders/{order_id}")
            if not order.get("success"):
                return order
            current_summary = redacted_send_summary(
                order.get("data"),
                company_party_id=self.configured_party_id,
                transport_type=str(challenge.summary_json["transport_type"]),
                strict_transport=bool(challenge.summary_json["strict_transport"]),
            )
            _raise_if_send_ineligible(current_summary)
            current_hash = hash_payload(current_summary)
            if current_hash != challenge.operation_hash or current_hash != operation_hash:
                raise LocalToolError(
                    "challenge_changed",
                    "Invoice state changed after the confirmation challenge was created",
                )
            self.consume_confirmation_challenge(
                challenge=challenge,
                confirmation_token=confirmation_token,
                operation_hash=current_hash,
            )
            headers = (
                {"StrictTransportType": "true"} if current_summary["strict_transport"] else None
            )
            return await client.request(
                "POST",
                "/orders/commands/send",
                json={
                    "Transporttype": current_summary["transport_type"],
                    "OrderIDs": [int(order_id)],
                },
                headers=headers,
            )

        return await self.execute_tool(
            tool_name="billit.invoice.confirm_send",
            operation_class="external_send",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
            resource_type="confirmation_challenge",
            resource_id=challenge_id,
        )

    async def invoice_get_delivery_status(self, *, order_id: int) -> dict[str, Any]:
        """Return a concise fresh-read delivery status."""

        async def handler() -> dict[str, Any]:
            client = await self.audited_client(tool_name="billit.invoice.get_delivery_status")
            order = await client.request("GET", f"/orders/{order_id}")
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

        return await self.execute_tool(
            tool_name="billit.invoice.get_delivery_status",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
            resource_type="order",
            resource_id=str(order_id),
        )

    async def invoice_summary(self, *, start_date: str, end_date: str) -> dict[str, Any]:
        """Return a read-only invoice summary through the shared service helper."""

        async def handler() -> dict[str, Any]:
            client = await self.audited_client(tool_name="billit.invoice.summary")
            return await generate_invoice_summary(client, start_date, end_date)

        return await self.execute_tool(
            tool_name="billit.invoice.summary",
            operation_class="read",
            handler=handler,
            company_party_id=self._configured_party_id_or_none(),
        )

    async def company_status(self, *, tool_name: str) -> CompanyStatus:
        """Fetch and parse accountInformation for the configured PartyID."""

        client = await self.audited_client(tool_name=tool_name)
        response = await client.request("GET", "/account/accountInformation")
        if not response.get("success"):
            return CompanyStatus(
                account_response=response,
                configured_party_id=self.settings().party_id,
                companies=[],
                company_ids=set(),
                parseable=False,
                authorized=False,
                warnings=["Billit accountInformation could not be read."],
            )
        configured_party_id = self.settings().party_id
        items = account_information_items(response.get("data"))
        companies = [_safe_company(item, configured_party_id) for item in items]
        company_ids = {
            str(company["company_party_id"])
            for company in companies
            if company.get("company_party_id") is not None
        }
        warnings: list[str] = []
        parseable = bool(items)
        if not company_ids:
            warnings.append(
                "accountInformation did not expose a parseable company list; reads are allowed, "
                "but writes and sends are blocked."
            )
        elif configured_party_id not in company_ids:
            warnings.append(
                "Configured BILLIT_PARTY_ID was not present in accountInformation; writes and "
                "sends are blocked."
            )
        return CompanyStatus(
            account_response=response,
            configured_party_id=configured_party_id,
            companies=companies,
            company_ids=company_ids,
            parseable=parseable,
            authorized=configured_party_id in company_ids,
            warnings=warnings,
        )

    async def validate_company_for_write(self, *, tool_name: str) -> None:
        """Require the configured PartyID to be verified before writes/sends."""

        company = await self.company_status(tool_name=tool_name)
        if not company.account_response.get("success"):
            raise LocalToolError(
                "company_entitlement_unverified",
                "Billit accountInformation must succeed before local writes or sends.",
                error_code="COMPANY_ENTITLEMENT_UNVERIFIED",
            )
        if company.authorized:
            return
        if company.company_ids:
            raise LocalToolError(
                "unauthorized_company",
                "Configured BILLIT_PARTY_ID is not authorized by accountInformation.",
                error_code="UNAUTHORIZED_COMPANY",
            )
        raise LocalToolError(
            "company_entitlement_unverified",
            "Company entitlement could not be parsed from accountInformation.",
            error_code="COMPANY_ENTITLEMENT_UNVERIFIED",
        )

    def create_confirmation_challenge(
        self,
        *,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        summary: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a server-owned local confirmation challenge."""

        challenge_id = str(uuid.uuid4())
        token = secrets.token_urlsafe(24)
        operation_hash = hash_payload(summary)
        expires_at = datetime.now(UTC) + timedelta(minutes=10)
        self.state.create_confirmation_challenge(
            challenge_id=challenge_id,
            confirmation_token_hash=hash_text(token),
            expires_at=expires_at,
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            company_party_id=self.configured_party_id,
            operation_hash=operation_hash,
            summary=summary,
        )
        self._audit_sync(
            event_type="confirmation_challenge_created",
            operation_class="confirmation",
            outcome="challenge_created",
            correlation_id=_token(),
            company_party_id=self.configured_party_id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary={"operation_type": operation_type, "resource_type": resource_type},
        )
        return {
            "challenge_id": challenge_id,
            "confirmation_token": token,
            "operation_hash": operation_hash,
            "expires_at": expires_at.isoformat(),
            "summary": summary,
        }

    def get_pending_confirmation_challenge(self, challenge_id: str) -> LocalConfirmationChallenge:
        """Load a pending challenge without consuming it."""

        challenge = self.state.get_confirmation_challenge(challenge_id)
        if challenge is None:
            raise LocalToolError("challenge_not_found", "Confirmation challenge not found")
        if challenge.status != "pending" or challenge.expires_at <= datetime.now(UTC):
            raise LocalToolError("challenge_expired", "Confirmation challenge is not pending")
        if challenge.company_party_id != self.configured_party_id:
            raise LocalToolError("challenge_mismatch", "Challenge company does not match")
        return challenge

    def consume_confirmation_challenge(
        self,
        *,
        challenge: LocalConfirmationChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Atomically consume a pending confirmation challenge."""

        if challenge.confirmation_token_hash != hash_text(confirmation_token):
            raise LocalToolError("challenge_token_invalid", "Confirmation token is invalid")
        consumed = self.state.consume_confirmation_challenge(
            challenge_id=challenge.challenge_id,
            confirmation_token_hash=hash_text(confirmation_token),
            operation_hash=operation_hash,
            operation_type=challenge.operation_type,
            resource_type=challenge.resource_type,
            resource_id=challenge.resource_id,
            company_party_id=self.configured_party_id,
        )
        if not consumed:
            raise LocalToolError("challenge_mismatch", "Confirmation was not consumed")
        self._audit_sync(
            event_type="confirmation_challenge_consumed",
            operation_class="confirmation",
            outcome="challenge_consumed",
            correlation_id=_token(),
            company_party_id=self.configured_party_id,
            resource_type=challenge.resource_type,
            resource_id=challenge.resource_id,
            summary={"operation_type": challenge.operation_type},
        )

    def _record_idempotency_started(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> LocalIdempotencyRecord | None:
        if not idempotency_key:
            return None
        record = self.state.record_idempotency_started(
            idempotency_id=str(uuid.uuid4()),
            company_party_id=self.configured_party_id,
            operation_type=operation_type,
            idempotency_key_hash=hash_text(idempotency_key),
            operation_hash=operation_hash,
        )
        if record.operation_hash != operation_hash:
            raise LocalToolError(
                "idempotency_conflict",
                "Idempotency key was already used for a different operation",
                error_code="IDEMPOTENCY_CONFLICT",
            )
        return record

    @property
    def local_writes_enabled(self) -> bool:
        """Return whether local draft writes are enabled."""

        return os.getenv("BILLIT_MCP_LOCAL_ALLOW_WRITES") == "1"

    @property
    def local_sends_enabled(self) -> bool:
        """Return whether external invoice sends are enabled."""

        return os.getenv("BILLIT_MCP_LOCAL_ALLOW_SENDS") == "1"

    def require_writes_enabled(self) -> None:
        """Fail unless draft creation has been explicitly enabled."""

        if not self.local_writes_enabled:
            raise LocalToolError(
                "local_writes_disabled",
                "Set BILLIT_MCP_LOCAL_ALLOW_WRITES=1 to allow local invoice draft creation.",
                error_code="LOCAL_WRITES_DISABLED",
            )

    def require_sends_enabled(self) -> None:
        """Fail unless invoice sending has been explicitly enabled."""

        if not self.local_sends_enabled:
            raise LocalToolError(
                "local_sends_disabled",
                "Set BILLIT_MCP_LOCAL_ALLOW_SENDS=1 to allow local invoice sending.",
                error_code="LOCAL_SENDS_DISABLED",
            )

    def local_warnings(self) -> list[str]:
        """Return local configuration warnings."""

        warnings: list[str] = []
        if os.getenv("BILLIT_CONTEXT_PARTY_ID"):
            warnings.append("BILLIT_CONTEXT_PARTY_ID is ignored; ContextPartyID is disabled.")
        if not self.settings().party_id.isdigit():
            warnings.append(
                "BILLIT_PARTY_ID is non-numeric; reads can run, but writes are blocked."
            )
        if environment_name(self.settings().base_url) != "sandbox":
            warnings.append("Local API-key runtime is pointed at a non-sandbox Billit base URL.")
        return warnings

    async def audit(
        self,
        *,
        event_type: str,
        operation_class: str,
        outcome: str,
        correlation_id: str,
        tool_name: str | None = None,
        environment: str | None = None,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        summary: dict[str, Any] | None = None,
        error_code: str | None = None,
        latency_ms: int | None = None,
    ) -> None:
        """Record a redacted audit event."""

        self.state.audit(
            audit_id=str(uuid.uuid4()),
            event_type=event_type,
            operation_class=operation_class,
            tool_name=tool_name,
            outcome=outcome,
            error_code=error_code,
            correlation_id=correlation_id,
            environment=environment or environment_name(self.settings().base_url),
            company_party_id=company_party_id,
            resource_type=resource_type,
            resource_id=resource_id,
            summary=summary,
            latency_ms=latency_ms,
        )

    def _audit_sync(
        self,
        *,
        event_type: str,
        operation_class: str,
        outcome: str,
        correlation_id: str,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        summary: dict[str, Any] | None = None,
        error_code: str | None = None,
    ) -> None:
        with suppress(Exception):
            self.state.audit(
                audit_id=str(uuid.uuid4()),
                event_type=event_type,
                operation_class=operation_class,
                tool_name=None,
                outcome=outcome,
                error_code=error_code,
                correlation_id=correlation_id,
                environment=environment_name(self.settings().base_url),
                company_party_id=company_party_id,
                resource_type=resource_type,
                resource_id=resource_id,
                summary=summary,
                latency_ms=None,
            )

    def _configured_party_id_or_none(self) -> int | None:
        with suppress(Exception):
            return self.configured_party_id
        return None


class LocalAuditedBillitClient:
    """Local Billit API client wrapper that records redacted outbound audit."""

    def __init__(
        self,
        *,
        client: LocalBillitClient,
        runtime: LocalAPIKeyRuntime,
        tool_name: str,
        environment: str,
        company_party_id: int | None,
    ) -> None:
        self._client = client
        self._runtime = runtime
        self._tool_name = tool_name
        self._environment = environment
        self._company_party_id = company_party_id

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        """Proxy a Billit request and audit only method/path/outcome metadata."""

        started = perf_counter()
        outcome = "success"
        error_code: str | None = None
        try:
            response = await self._client.request(method, url, **kwargs)
            if not response.get("success", False):
                outcome = "failure"
                error_code = str(response.get("error_code") or "BILLIT_API_ERROR")
            return response
        except Exception:
            outcome = "failure"
            error_code = "BILLIT_API_EXCEPTION"
            raise
        finally:
            with suppress(Exception):
                await self._runtime.audit(
                    event_type="billit_api_call",
                    operation_class="external_api",
                    outcome=outcome,
                    correlation_id=_token(),
                    tool_name=self._tool_name,
                    environment=self._environment,
                    company_party_id=self._company_party_id,
                    summary={"method": method.upper(), "path": url},
                    error_code=error_code,
                    latency_ms=int((perf_counter() - started) * 1000),
                )


def success(data: Any) -> dict[str, Any]:
    """Return a successful local tool result."""

    return {"success": True, "data": data, "error": None, "error_code": None}


def failure(error: Any, error_code: str) -> dict[str, Any]:
    """Return a failed local tool result."""

    return {"success": False, "data": None, "error": error, "error_code": error_code}


def error_result(exc: Exception) -> dict[str, Any]:
    """Convert an exception into the stable MCP envelope."""

    if isinstance(exc, LocalToolError):
        return exc.to_result()
    return failure(
        {
            "type": "local_tool_error",
            "severity": "blocking",
            "retryable": False,
            "user_action_required": True,
            "message": str(exc),
        },
        "LOCAL_TOOL_ERROR",
    )


def hash_payload(payload: dict[str, Any]) -> str:
    """Return a stable hash for a JSON-compatible operation payload."""

    return hash_text(json.dumps(payload, sort_keys=True, separators=(",", ":")))


def hash_text(value: str) -> str:
    """Return a SHA-256 hex digest for local redaction and idempotency."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def environment_name(base_url: str) -> str:
    """Classify the Billit target environment without exposing credentials."""

    if "sandbox" in base_url:
        return "sandbox"
    if "api.billit.be" in base_url:
        return "production"
    return "custom"


def missing_local_settings() -> list[str]:
    """Return missing required local API-key env var names without reading secrets."""

    return [
        name
        for name in ("BILLIT_API_KEY", "BILLIT_BASE_URL", "BILLIT_PARTY_ID")
        if not os.getenv(name)
    ]


def base_url_host(base_url: str) -> str:
    """Return the configured Billit host without credentials."""

    parsed = urlparse(base_url)
    return parsed.netloc or base_url.replace("https://", "").replace("http://", "").split("/")[0]


def _local_settings(settings: BillitSettings) -> BillitSettings:
    """Return explicit API-key settings with ContextPartyID disabled."""

    return BillitSettings(
        base_url=settings.base_url,
        api_key=settings.api_key,
        party_id=settings.party_id,
        context_party_id=None,
        rate_limit_per_minute=settings.rate_limit_per_minute,
    )


def account_information_items(data: Any) -> list[dict[str, Any]]:
    """Return likely company items from Billit accountInformation payloads."""

    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    items: list[dict[str, Any]] = []
    for key in ("Items", "items", "value", "Companies", "companies", "Company", "company"):
        value = data.get(key)
        if isinstance(value, list):
            items.extend(item for item in value if isinstance(item, dict))
        elif isinstance(value, dict):
            items.append(value)
    items.append(data)
    return items


def redacted_send_summary(
    order: Any,
    *,
    company_party_id: int,
    transport_type: str,
    strict_transport: bool,
) -> dict[str, Any]:
    """Build a canonical redacted summary for invoice-send confirmation."""

    raw = build_send_summary(
        order,
        company_party_id=company_party_id,
        transport_type=transport_type,
        strict_transport=strict_transport,
    )
    return {
        "company_party_id": raw["company_party_id"],
        "order_id": raw["order_id"],
        "invoice_number": raw["invoice_number"],
        "customer_name_hash": hash_text(str(raw.get("customer_name") or "")),
        "customer_vat_hash": hash_text(str(raw.get("customer_vat") or "")),
        "amount_including_vat": raw["amount_including_vat"],
        "currency": raw["currency"],
        "is_sent": raw["is_sent"],
        "order_status": raw["order_status"],
        "transport_type": raw["transport_type"],
        "strict_transport": raw["strict_transport"],
        "fallback_allowed": raw["fallback_allowed"],
    }


def _safe_company(item: dict[str, Any], configured_party_id: str) -> dict[str, Any]:
    party_id = _extract_party_id(item)
    return {
        "company_party_id": party_id,
        "name": item.get("Name") or item.get("CompanyName") or item.get("name"),
        "is_configured": str(party_id) == configured_party_id if party_id is not None else False,
    }


def _extract_party_id(item: dict[str, Any]) -> int | None:
    for key in ("PartyID", "CompanyPartyID", "CompanyID", "ID", "party_id", "company_party_id"):
        value = item.get(key)
        if value is None:
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


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
        raise LocalToolError("invoice_send_ineligible", "Order ID is missing from Billit order")
    if summary.get("is_sent"):
        raise LocalToolError("invoice_already_sent", "Invoice is already marked as sent")


def _transport_type(value: str) -> str:
    return "SMTP" if value == "Email" else value


def _validate_report_request(
    report_id: str,
    parameters: dict[str, str | int | float | bool],
) -> None:
    if not report_id or "/" in report_id or "\\" in report_id or "$" in report_id:
        raise LocalToolError("invalid_report_id", "report_id must be a simple Billit report id")
    for key, value in parameters.items():
        if key.startswith("$") or "filter" in key.lower():
            raise LocalToolError(
                "unsupported_report_parameter", "Raw OData parameters are rejected"
            )
        if not isinstance(value, str | int | float | bool):
            raise LocalToolError(
                "unsupported_report_parameter",
                "Report parameters must be scalar values",
            )


def _client_is_closed(client: LocalBillitClient) -> bool:
    inner = getattr(client, "client", None)
    return bool(getattr(inner, "is_closed", False))


def _token() -> str:
    return secrets.token_urlsafe(18)
