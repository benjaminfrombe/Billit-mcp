"""Local API-key company entitlement parsing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from billit_mcp.local_api_key.common import LocalToolError, ToolResult


class CompanyRuntime(Protocol):
    """Runtime hooks required by local company entitlement checks."""

    @property
    def configured_party_id(self) -> int:
        """Configured Billit PartyID."""
        ...

    def settings_party_id(self) -> str:
        """Configured PartyID as supplied in settings."""
        ...

    async def audited_client(self, *, tool_name: str) -> Any:
        """Return an audited Billit client."""
        ...


@dataclass(frozen=True)
class CompanyStatus:
    """Parsed accountInformation entitlement state for the configured PartyID."""

    account_response: ToolResult
    configured_party_id: str
    companies: list[dict[str, Any]]
    company_ids: set[str]
    parseable: bool
    authorized: bool
    warnings: list[str]

    @property
    def state(self) -> str:
        """Return the user-facing authorization state."""

        if self.authorized:
            return "verified"
        if self.company_ids:
            return "unauthorized"
        return "inconclusive"


class LocalCompanyService:
    """Resolve and validate companies from Billit accountInformation."""

    def __init__(self, runtime: CompanyRuntime) -> None:
        self.runtime = runtime

    async def company_status(self, *, tool_name: str) -> CompanyStatus:
        """Fetch and parse accountInformation for the configured PartyID."""

        client = await self.runtime.audited_client(tool_name=tool_name)
        response = await client.request("GET", "/account/accountInformation")
        configured_party_id = self.runtime.settings_party_id()
        if not response.get("success"):
            return CompanyStatus(
                account_response=response,
                configured_party_id=configured_party_id,
                companies=[],
                company_ids=set(),
                parseable=False,
                authorized=False,
                warnings=["Billit accountInformation could not be read."],
            )
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
