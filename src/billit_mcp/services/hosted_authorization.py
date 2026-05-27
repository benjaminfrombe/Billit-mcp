"""Hosted connection and company authorization helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sqlalchemy import select

from billit_mcp.persistence.models import BillitCompany, BillitConnection
from billit_mcp.services.hosted_errors import HostedToolError

if TYPE_CHECKING:
    from billit_mcp.persistence.database import HostedDatabase


class HostedAuthorizationService:
    """Authorize hosted Billit connections and company PartyIDs."""

    def __init__(self, database: HostedDatabase) -> None:
        self._database = database

    async def resolve_connection(
        self,
        *,
        actor_id: str,
        environment: str,
    ) -> BillitConnection:
        """Return the active Billit connection for an actor/environment."""

        async with self._database.session() as session:
            connection = await session.scalar(
                select(BillitConnection).where(
                    BillitConnection.actor_id == actor_id,
                    BillitConnection.environment == environment,
                )
            )
            if connection is None:
                raise HostedToolError(
                    "billit_not_connected",
                    f"No Billit OAuth connection exists for {environment}",
                )
            if connection.status != "active":
                raise HostedToolError(
                    "billit_reauthorization_required",
                    "Billit connection requires reauthorization",
                )
            session.expunge(connection)
            return connection

    async def validate_company(
        self,
        *,
        connection_id: str,
        environment: str,
        company_party_id: int,
    ) -> None:
        """Fail unless the company is authorized for this connection."""

        async with self._database.session() as session:
            company = await session.scalar(
                select(BillitCompany).where(
                    BillitCompany.connection_id == connection_id,
                    BillitCompany.environment == environment,
                    BillitCompany.company_party_id == company_party_id,
                    BillitCompany.active.is_(True),
                )
            )
        if company is None:
            raise HostedToolError(
                "unauthorized_company",
                "company_party_id is not authorized for this Billit connection",
                error_code="UNAUTHORIZED_COMPANY",
            )

    async def list_authorized_companies(
        self,
        *,
        connection_id: str,
        environment: str,
    ) -> list[dict[str, Any]]:
        """Return sanitized company rows authorized for a hosted connection."""

        async with self._database.session() as session:
            companies = (
                await session.scalars(
                    select(BillitCompany).where(
                        BillitCompany.connection_id == connection_id,
                        BillitCompany.environment == environment,
                        BillitCompany.active.is_(True),
                    )
                )
            ).all()
        return [
            {
                "company_party_id": company.company_party_id,
                "environment": company.environment,
                "active": company.active,
                "is_default": company.is_default,
            }
            for company in companies
        ]
