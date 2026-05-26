"""SQLAlchemy models for hosted Billit MCP mode."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def now_utc() -> datetime:
    """Return a timezone-aware UTC timestamp."""

    return datetime.now(UTC)


def new_id() -> str:
    """Return a compact random identifier."""

    return uuid.uuid4().hex


class Base(DeclarativeBase):
    """Declarative base for hosted persistence."""


class Actor(Base):
    """Local hosted user identity."""

    __tablename__ = "actors"

    actor_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    subject_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    display_email_ciphertext: Mapped[str | None] = mapped_column(Text)
    display_email_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    disabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OAuthClient(Base):
    """Static MCP OAuth client."""

    __tablename__ = "oauth_clients"

    client_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    client_name: Mapped[str] = mapped_column(String(255), default="Billit MCP client")
    client_type: Mapped[str] = mapped_column(String(32), default="public")
    client_secret_hash: Mapped[str | None] = mapped_column(String(128))
    redirect_uris: Mapped[list[str]] = mapped_column(JSON)
    allowed_scopes: Mapped[list[str]] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(32), default="active", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc
    )
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OAuthAuthorizationTransaction(Base):
    """MCP authorization transaction linking Billit connect and code issuance."""

    __tablename__ = "oauth_authorization_transactions"

    transaction_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    client_id: Mapped[str] = mapped_column(ForeignKey("oauth_clients.client_id"), index=True)
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("actors.actor_id"), index=True)
    redirect_uri: Mapped[str] = mapped_column(Text)
    scopes: Mapped[list[str]] = mapped_column(JSON)
    state_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    environment: Mapped[str] = mapped_column(String(32), default="sandbox")
    billit_connection_id: Mapped[str | None] = mapped_column(String(64), index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class OAuthAuthCode(Base):
    """One-time MCP authorization code."""

    __tablename__ = "oauth_auth_codes"

    code_hash: Mapped[str] = mapped_column(String(128), primary_key=True)
    client_id: Mapped[str] = mapped_column(ForeignKey("oauth_clients.client_id"), index=True)
    actor_id: Mapped[str] = mapped_column(ForeignKey("actors.actor_id"), index=True)
    redirect_uri: Mapped[str] = mapped_column(Text)
    code_challenge: Mapped[str] = mapped_column(String(255))
    code_challenge_method: Mapped[str] = mapped_column(String(16), default="S256")
    scopes: Mapped[list[str]] = mapped_column(JSON)
    state_hash: Mapped[str | None] = mapped_column(String(128))
    nonce_hash: Mapped[str | None] = mapped_column(String(128))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class OAuthTokenRevocation(Base):
    """Revoked MCP access token JTI."""

    __tablename__ = "oauth_token_revocations"

    jti_hash: Mapped[str] = mapped_column(String(128), primary_key=True)
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("actors.actor_id"), index=True)
    client_id: Mapped[str | None] = mapped_column(ForeignKey("oauth_clients.client_id"), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    reason: Mapped[str | None] = mapped_column(String(255))


class BillitConnection(Base):
    """Billit OAuth connection for one actor and environment."""

    __tablename__ = "billit_connections"
    __table_args__ = (
        UniqueConstraint("actor_id", "environment", name="uq_billit_connection_actor_env"),
    )

    connection_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    actor_id: Mapped[str] = mapped_column(ForeignKey("actors.actor_id"), index=True)
    environment: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), default="pending_oauth_exchange", index=True)
    billit_subject_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    billit_account_fingerprint_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    connected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_refresh_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reauthorization_required_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class BillitOAuthGrant(Base):
    """Encrypted Billit OAuth grant material."""

    __tablename__ = "billit_oauth_grants"

    connection_id: Mapped[str] = mapped_column(
        ForeignKey("billit_connections.connection_id"), primary_key=True
    )
    access_token_ciphertext: Mapped[str] = mapped_column(Text)
    access_token_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    refresh_token_ciphertext: Mapped[str] = mapped_column(Text)
    refresh_token_hash: Mapped[str] = mapped_column(String(128), unique=True)
    refresh_token_version: Mapped[int] = mapped_column(Integer, default=1)
    encryption_key_version: Mapped[str] = mapped_column(String(64), default="v1")
    encryption_context: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc
    )


class BillitCompany(Base):
    """Authorized Billit company for a connection."""

    __tablename__ = "billit_companies"
    __table_args__ = (
        UniqueConstraint(
            "connection_id",
            "environment",
            "company_party_id",
            name="uq_billit_company_connection_env_party",
        ),
        Index("ix_billit_companies_active", "connection_id", "active"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    connection_id: Mapped[str] = mapped_column(ForeignKey("billit_connections.connection_id"))
    environment: Mapped[str] = mapped_column(String(32), index=True)
    company_party_id: Mapped[int] = mapped_column(Integer, index=True)
    company_name_ciphertext: Mapped[str | None] = mapped_column(Text)
    company_name_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    vat_number_hash: Mapped[str | None] = mapped_column(String(128), index=True)
    role: Mapped[str] = mapped_column(String(32), default="unknown")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class ConfirmationChallenge(Base):
    """Server-owned confirmation challenge for consequential operations."""

    __tablename__ = "confirmation_challenges"

    challenge_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    actor_id: Mapped[str] = mapped_column(ForeignKey("actors.actor_id"), index=True)
    client_id: Mapped[str] = mapped_column(ForeignKey("oauth_clients.client_id"), index=True)
    connection_id: Mapped[str] = mapped_column(ForeignKey("billit_connections.connection_id"))
    environment: Mapped[str] = mapped_column(String(32))
    company_party_id: Mapped[int] = mapped_column(Integer, index=True)
    operation_type: Mapped[str] = mapped_column(String(64), index=True)
    resource_type: Mapped[str | None] = mapped_column(String(64))
    resource_id: Mapped[str | None] = mapped_column(String(255), index=True)
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    operation_hash: Mapped[str] = mapped_column(String(128), index=True)
    required_scope: Mapped[str] = mapped_column(String(128))
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    nonce_hash: Mapped[str] = mapped_column(String(128), unique=True)
    confirmation_token_hash: Mapped[str] = mapped_column(String(128), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class IdempotencyRecord(Base):
    """Local idempotency guard for hosted write operations."""

    __tablename__ = "idempotency_records"
    __table_args__ = (
        UniqueConstraint(
            "connection_id",
            "company_party_id",
            "operation_type",
            "idempotency_key_hash",
            name="uq_idempotency_connection_company_operation_key",
        ),
    )

    idempotency_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    idempotency_key_hash: Mapped[str] = mapped_column(String(128), index=True)
    connection_id: Mapped[str] = mapped_column(ForeignKey("billit_connections.connection_id"))
    company_party_id: Mapped[int] = mapped_column(Integer, index=True)
    operation_type: Mapped[str] = mapped_column(String(64), index=True)
    operation_hash: Mapped[str] = mapped_column(String(128), index=True)
    status: Mapped[str] = mapped_column(String(32), default="started", index=True)
    billit_resource_type: Mapped[str | None] = mapped_column(String(64))
    billit_resource_id: Mapped[str | None] = mapped_column(String(255), index=True)
    billit_error_code: Mapped[str | None] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc
    )


class AuditEvent(Base):
    """Redacted hosted audit event."""

    __tablename__ = "audit_events"
    __table_args__ = (
        Index("ix_audit_actor_created", "actor_id", "created_at"),
        Index("ix_audit_company_created", "company_party_id", "created_at"),
    )

    audit_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=new_id)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("actors.actor_id"), index=True)
    client_id: Mapped[str | None] = mapped_column(ForeignKey("oauth_clients.client_id"), index=True)
    connection_id: Mapped[str | None] = mapped_column(String(64), index=True)
    environment: Mapped[str | None] = mapped_column(String(32), index=True)
    company_party_id: Mapped[int | None] = mapped_column(Integer, index=True)
    event_type: Mapped[str] = mapped_column(String(128), index=True)
    operation_class: Mapped[str] = mapped_column(String(64), index=True)
    tool_name: Mapped[str | None] = mapped_column(String(128), index=True)
    resource_refs: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    request_hash: Mapped[str | None] = mapped_column(String(128))
    response_hash: Mapped[str | None] = mapped_column(String(128))
    summary_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    outcome: Mapped[str] = mapped_column(String(64), index=True)
    error_code: Mapped[str | None] = mapped_column(String(128), index=True)
    correlation_id: Mapped[str] = mapped_column(String(128), index=True)
    billit_request_id: Mapped[str | None] = mapped_column(String(255))
    ip_hash: Mapped[str | None] = mapped_column(String(128))
    user_agent_hash: Mapped[str | None] = mapped_column(String(128))
    latency_ms: Mapped[int | None] = mapped_column(Integer)
