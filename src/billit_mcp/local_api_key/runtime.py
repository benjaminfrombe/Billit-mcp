"""Local/private API-key runtime facade for curated stdio MCP tools."""

from __future__ import annotations

import os
import uuid
from contextlib import suppress
from time import perf_counter
from typing import Any, cast

from billit.client import BillitAPIClient, BillitSettings
from billit_mcp.local_api_key.client import LocalAuditedBillitClient, client_is_closed
from billit_mcp.local_api_key.common import (
    LOCAL_API_KEY_TOOL_NAMES,
    SECURITY_DENIALS,
    LocalBillitClient,
    LocalToolError,
    ToolResult,
    error_result,
    failure,
    hash_payload,
    hash_text,
    item_list,
    success,
    token,
)
from billit_mcp.local_api_key.companies import CompanyStatus, LocalCompanyService
from billit_mcp.local_api_key.invoice_tools import LocalInvoiceTools
from billit_mcp.local_api_key.read_tools import LocalReadTools
from billit_mcp.local_api_key.settings import (
    environment_name,
    local_settings_without_context,
    local_warnings,
    missing_local_settings,
    settings_from_env,
)
from billit_mcp.local_api_key.state import LocalConfirmationChallenge, LocalStateStore
from billit_mcp.local_api_key.state_services import LocalWorkflowState
from billit_mcp.services.invoice_workflow import (
    IdempotencyStart,
    PendingSendChallenge,
    SendChallenge,
    redacted_send_summary,
)


class LocalAPIKeyRuntime:
    """Runtime shared by the local/private API-key MCP tools."""

    def __init__(
        self,
        *,
        settings: BillitSettings | None = None,
        state: LocalStateStore | None = None,
        client_factory: Any = BillitAPIClient,
    ) -> None:
        self._settings = local_settings_without_context(settings) if settings is not None else None
        self.state = state or LocalStateStore(
            os.getenv("BILLIT_MCP_LOCAL_STATE_DB", ".local/billit-mcp-api-key-state.db")
        )
        self.client_factory = client_factory
        self._client: LocalBillitClient | None = None
        self._companies = LocalCompanyService(self)
        self._workflow_state = LocalWorkflowState(self)
        self._read_tools = LocalReadTools(self)
        self._invoice_tools = LocalInvoiceTools(self)

    async def get_client(self) -> LocalBillitClient:
        """Return the process-scoped explicit API-key Billit client."""

        if self._client is None or client_is_closed(self._client):
            self._client = self.client_factory(self.settings())
        return self._client

    async def close(self) -> None:
        """Close the cached Billit client."""

        if self._client is not None:
            await self._client.close()
            self._client = None

    def settings(self) -> BillitSettings:
        """Return explicit local API-key settings with ContextPartyID disabled."""

        if self._settings is None:
            self._settings = settings_from_env()
        return self._settings

    def settings_party_id(self) -> str:
        """Return the configured Billit PartyID without coercion."""

        return self.settings().party_id

    def settings_base_url(self) -> str:
        """Return the configured Billit base URL."""

        return self.settings().base_url

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

    async def execute_tool(
        self,
        *,
        tool_name: str,
        operation_class: str,
        handler: Any,
        company_party_id: int | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
    ) -> ToolResult:
        """Run a local tool with centralized structured errors and audit."""

        started = perf_counter()
        outcome = "success"
        error_code: str | None = None
        correlation_id = token()
        try:
            result = cast("ToolResult", await handler())
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
            company_party_id=self.configured_party_id_or_none(),
        )

    async def company_status(self, *, tool_name: str) -> CompanyStatus:
        """Fetch and parse accountInformation for the configured PartyID."""

        return await self._companies.company_status(tool_name=tool_name)

    async def validate_company_for_write(self, *, tool_name: str) -> None:
        """Require the configured PartyID to be verified before writes/sends."""

        await self._companies.validate_company_for_write(tool_name=tool_name)

    def create_confirmation_challenge(
        self,
        *,
        operation_type: str,
        resource_type: str,
        resource_id: str,
        summary: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a server-owned local confirmation challenge."""

        return self._workflow_state.create_confirmation_challenge(
            operation_type=operation_type,
            resource_type=resource_type,
            resource_id=resource_id,
            summary=summary,
        ).to_result()

    def get_pending_confirmation_challenge(self, challenge_id: str) -> LocalConfirmationChallenge:
        """Load a pending challenge without consuming it."""

        return self._workflow_state.get_pending_confirmation_challenge(challenge_id)

    def consume_confirmation_challenge(
        self,
        *,
        challenge: LocalConfirmationChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Atomically consume a pending confirmation challenge."""

        self._workflow_state.consume_confirmation_challenge(
            challenge=challenge,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
        )

    async def local_idempotency_state(
        self,
        *,
        operation_type: str,
        idempotency_key: str | None,
        operation_hash: str,
    ) -> IdempotencyStart | None:
        """Create or return local idempotency state for the shared workflow."""

        return await self._workflow_state.idempotency_state(
            operation_type=operation_type,
            idempotency_key=idempotency_key,
            operation_hash=operation_hash,
        )

    async def record_local_idempotency_outcome(
        self,
        *,
        idempotency_id: str,
        status: str,
        billit_resource_type: str | None = None,
        billit_resource_id: str | None = None,
        billit_error_code: str | None = None,
    ) -> None:
        """Persist local idempotency outcome for the shared workflow."""

        await self._workflow_state.record_idempotency_outcome(
            idempotency_id=idempotency_id,
            status=status,
            billit_resource_type=billit_resource_type,
            billit_resource_id=billit_resource_id,
            billit_error_code=billit_error_code,
        )

    def create_local_send_challenge(
        self,
        *,
        resource_id: str,
        summary: dict[str, Any],
    ) -> SendChallenge:
        """Create a local invoice-send confirmation challenge."""

        return self._workflow_state.create_confirmation_challenge(
            operation_type="invoice_send",
            resource_type="order",
            resource_id=resource_id,
            summary=summary,
        )

    def get_pending_local_send_challenge(self, *, challenge_id: str) -> PendingSendChallenge:
        """Load a pending local invoice-send challenge."""

        return self._workflow_state.get_pending_send_challenge(challenge_id)

    def consume_local_send_challenge(
        self,
        *,
        challenge: PendingSendChallenge,
        confirmation_token: str,
        operation_hash: str,
    ) -> None:
        """Atomically consume a local invoice-send challenge."""

        self._workflow_state.consume_send_challenge(
            challenge=challenge,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
        )

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

        return local_warnings(self.settings())

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

    def audit_sync(
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
        """Record a redacted audit event from synchronous helpers."""

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

    def _audit_sync(self, **kwargs: Any) -> None:
        """Backward-compatible alias for older local helpers."""

        self.audit_sync(**kwargs)

    def configured_party_id_or_none(self) -> int | None:
        """Return the numeric configured PartyID when it is valid."""

        with suppress(Exception):
            return self.configured_party_id
        return None

    def _configured_party_id_or_none(self) -> int | None:
        """Backward-compatible alias for older tests/helpers."""

        return self.configured_party_id_or_none()

    async def connection_status(self) -> ToolResult:
        return await self._read_tools.connection_status()

    async def list_companies(self) -> ToolResult:
        return await self._read_tools.list_companies()

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
    ) -> ToolResult:
        return await self._read_tools.search_orders(
            direction=direction,
            order_type=order_type,
            customer_name=customer_name,
            vat_number=vat_number,
            paid=paid,
            modified_since=modified_since,
            limit=limit,
        )

    async def get_order(self, *, order_id: int) -> ToolResult:
        return await self._read_tools.get_order(order_id=order_id)

    async def resolve_party(
        self,
        *,
        role: str,
        name: str | None = None,
        vat_number: str | None = None,
        email: str | None = None,
        external_provider_id: str | None = None,
    ) -> ToolResult:
        return await self._read_tools.resolve_party(
            role=role,
            name=name,
            vat_number=vat_number,
            email=email,
            external_provider_id=external_provider_id,
        )

    async def lookup_peppol_receiver(self, *, identifier: str) -> ToolResult:
        return await self._read_tools.lookup_peppol_receiver(identifier=identifier)

    async def list_financial_transactions(self, *, limit: int = 20) -> ToolResult:
        return await self._read_tools.list_financial_transactions(limit=limit)

    async def list_reports(self) -> ToolResult:
        return await self._read_tools.list_reports()

    async def get_report(
        self,
        *,
        report_id: str,
        parameters: dict[str, str | int | float | bool] | None = None,
    ) -> ToolResult:
        return await self._read_tools.get_report(report_id=report_id, parameters=parameters)

    async def invoice_prepare(
        self,
        *,
        customer: dict[str, Any],
        lines: list[dict[str, Any]],
        order_date: str,
        expiry_date: str,
        desired_transport: str | None = None,
    ) -> ToolResult:
        return await self._invoice_tools.invoice_prepare(
            customer=customer,
            lines=lines,
            order_date=order_date,
            expiry_date=expiry_date,
            desired_transport=desired_transport,
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
    ) -> ToolResult:
        return await self._invoice_tools.invoice_create_draft(
            customer=customer,
            lines=lines,
            order_date=order_date,
            expiry_date=expiry_date,
            external_provider_id=external_provider_id,
            idempotency_key=idempotency_key,
        )

    async def invoice_prepare_send(
        self,
        *,
        order_id: int,
        transport_type: str,
        strict_transport: bool = True,
    ) -> ToolResult:
        return await self._invoice_tools.invoice_prepare_send(
            order_id=order_id,
            transport_type=transport_type,
            strict_transport=strict_transport,
        )

    async def invoice_confirm_send(
        self,
        *,
        challenge_id: str,
        confirmation_token: str,
        operation_hash: str,
    ) -> ToolResult:
        return await self._invoice_tools.invoice_confirm_send(
            challenge_id=challenge_id,
            confirmation_token=confirmation_token,
            operation_hash=operation_hash,
        )

    async def invoice_get_delivery_status(self, *, order_id: int) -> ToolResult:
        return await self._read_tools.invoice_get_delivery_status(order_id=order_id)

    async def invoice_summary(self, *, start_date: str, end_date: str) -> ToolResult:
        return await self._read_tools.invoice_summary(start_date=start_date, end_date=end_date)


def _items(data: Any) -> list[dict[str, Any]]:
    """Backward-compatible list response helper."""

    return item_list(data)


__all__ = [
    "LOCAL_API_KEY_TOOL_NAMES",
    "CompanyStatus",
    "LocalAPIKeyRuntime",
    "LocalAuditedBillitClient",
    "LocalBillitClient",
    "LocalToolError",
    "error_result",
    "failure",
    "hash_payload",
    "hash_text",
    "missing_local_settings",
    "redacted_send_summary",
    "success",
]
