"""hosted oauth schema

Revision ID: 20260526_0001
Revises:
Create Date: 2026-05-26
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260526_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create hosted OAuth tables with explicit DDL."""

    op.create_table(
        "actors",
        sa.Column("actor_id", sa.String(length=64), nullable=False),
        sa.Column("subject_hash", sa.String(length=128), nullable=False),
        sa.Column("display_email_ciphertext", sa.Text(), nullable=True),
        sa.Column("display_email_hash", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("disabled_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("actor_id"),
        sa.UniqueConstraint("subject_hash"),
    )
    op.create_index("ix_actors_subject_hash", "actors", ["subject_hash"])
    op.create_index("ix_actors_display_email_hash", "actors", ["display_email_hash"])

    op.create_table(
        "oauth_clients",
        sa.Column("client_id", sa.String(length=255), nullable=False),
        sa.Column("client_name", sa.String(length=255), nullable=False),
        sa.Column("client_type", sa.String(length=32), nullable=False),
        sa.Column("client_secret_hash", sa.String(length=128), nullable=True),
        sa.Column("redirect_uris", sa.JSON(), nullable=False),
        sa.Column("allowed_scopes", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("client_id"),
    )
    op.create_index("ix_oauth_clients_status", "oauth_clients", ["status"])

    op.create_table(
        "oauth_authorization_transactions",
        sa.Column("transaction_id", sa.String(length=64), nullable=False),
        sa.Column("client_id", sa.String(length=255), nullable=False),
        sa.Column("actor_id", sa.String(length=64), nullable=True),
        sa.Column("redirect_uri", sa.Text(), nullable=False),
        sa.Column("scopes", sa.JSON(), nullable=False),
        sa.Column("state_hash", sa.String(length=128), nullable=True),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("billit_connection_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["actor_id"], ["actors.actor_id"]),
        sa.ForeignKeyConstraint(["client_id"], ["oauth_clients.client_id"]),
        sa.PrimaryKeyConstraint("transaction_id"),
    )
    op.create_index(
        "ix_oauth_authorization_transactions_actor_id",
        "oauth_authorization_transactions",
        ["actor_id"],
    )
    op.create_index(
        "ix_oauth_authorization_transactions_billit_connection_id",
        "oauth_authorization_transactions",
        ["billit_connection_id"],
    )
    op.create_index(
        "ix_oauth_authorization_transactions_client_id",
        "oauth_authorization_transactions",
        ["client_id"],
    )
    op.create_index(
        "ix_oauth_authorization_transactions_expires_at",
        "oauth_authorization_transactions",
        ["expires_at"],
    )
    op.create_index(
        "ix_oauth_authorization_transactions_state_hash",
        "oauth_authorization_transactions",
        ["state_hash"],
    )
    op.create_index(
        "ix_oauth_authorization_transactions_status",
        "oauth_authorization_transactions",
        ["status"],
    )

    op.create_table(
        "oauth_auth_codes",
        sa.Column("code_hash", sa.String(length=128), nullable=False),
        sa.Column("client_id", sa.String(length=255), nullable=False),
        sa.Column("actor_id", sa.String(length=64), nullable=False),
        sa.Column("redirect_uri", sa.Text(), nullable=False),
        sa.Column("code_challenge", sa.String(length=255), nullable=False),
        sa.Column("code_challenge_method", sa.String(length=16), nullable=False),
        sa.Column("scopes", sa.JSON(), nullable=False),
        sa.Column("state_hash", sa.String(length=128), nullable=True),
        sa.Column("nonce_hash", sa.String(length=128), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["actor_id"], ["actors.actor_id"]),
        sa.ForeignKeyConstraint(["client_id"], ["oauth_clients.client_id"]),
        sa.PrimaryKeyConstraint("code_hash"),
    )
    op.create_index("ix_oauth_auth_codes_actor_id", "oauth_auth_codes", ["actor_id"])
    op.create_index("ix_oauth_auth_codes_client_id", "oauth_auth_codes", ["client_id"])
    op.create_index("ix_oauth_auth_codes_expires_at", "oauth_auth_codes", ["expires_at"])
    op.create_index("ix_oauth_auth_codes_used_at", "oauth_auth_codes", ["used_at"])

    op.create_table(
        "oauth_token_revocations",
        sa.Column("jti_hash", sa.String(length=128), nullable=False),
        sa.Column("actor_id", sa.String(length=64), nullable=True),
        sa.Column("client_id", sa.String(length=255), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["actors.actor_id"]),
        sa.ForeignKeyConstraint(["client_id"], ["oauth_clients.client_id"]),
        sa.PrimaryKeyConstraint("jti_hash"),
    )
    op.create_index(
        "ix_oauth_token_revocations_actor_id",
        "oauth_token_revocations",
        ["actor_id"],
    )
    op.create_index(
        "ix_oauth_token_revocations_client_id",
        "oauth_token_revocations",
        ["client_id"],
    )
    op.create_index(
        "ix_oauth_token_revocations_expires_at",
        "oauth_token_revocations",
        ["expires_at"],
    )

    op.create_table(
        "billit_connections",
        sa.Column("connection_id", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=64), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("billit_subject_hash", sa.String(length=128), nullable=True),
        sa.Column("billit_account_fingerprint_hash", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("connected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_refresh_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reauthorization_required_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["actors.actor_id"]),
        sa.PrimaryKeyConstraint("connection_id"),
        sa.UniqueConstraint("actor_id", "environment", name="uq_billit_connection_actor_env"),
    )
    op.create_index("ix_billit_connections_actor_id", "billit_connections", ["actor_id"])
    op.create_index(
        "ix_billit_connections_billit_account_fingerprint_hash",
        "billit_connections",
        ["billit_account_fingerprint_hash"],
    )
    op.create_index(
        "ix_billit_connections_billit_subject_hash",
        "billit_connections",
        ["billit_subject_hash"],
    )
    op.create_index(
        "ix_billit_connections_environment",
        "billit_connections",
        ["environment"],
    )
    op.create_index("ix_billit_connections_status", "billit_connections", ["status"])

    op.create_table(
        "billit_oauth_grants",
        sa.Column("connection_id", sa.String(length=64), nullable=False),
        sa.Column("access_token_ciphertext", sa.Text(), nullable=False),
        sa.Column("access_token_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("refresh_token_ciphertext", sa.Text(), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=128), nullable=False),
        sa.Column("refresh_token_version", sa.Integer(), nullable=False),
        sa.Column("encryption_key_version", sa.String(length=64), nullable=False),
        sa.Column("encryption_context", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["connection_id"], ["billit_connections.connection_id"]),
        sa.PrimaryKeyConstraint("connection_id"),
        sa.UniqueConstraint("refresh_token_hash"),
    )
    op.create_index(
        "ix_billit_oauth_grants_access_token_expires_at",
        "billit_oauth_grants",
        ["access_token_expires_at"],
    )

    op.create_table(
        "billit_companies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("connection_id", sa.String(length=64), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("company_party_id", sa.Integer(), nullable=False),
        sa.Column("company_name_ciphertext", sa.Text(), nullable=True),
        sa.Column("company_name_hash", sa.String(length=128), nullable=True),
        sa.Column("vat_number_hash", sa.String(length=128), nullable=True),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_default", sa.Boolean(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["connection_id"], ["billit_connections.connection_id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "connection_id",
            "environment",
            "company_party_id",
            name="uq_billit_company_connection_env_party",
        ),
    )
    op.create_index("ix_billit_companies_active", "billit_companies", ["connection_id", "active"])
    op.create_index(
        "ix_billit_companies_company_name_hash",
        "billit_companies",
        ["company_name_hash"],
    )
    op.create_index(
        "ix_billit_companies_company_party_id",
        "billit_companies",
        ["company_party_id"],
    )
    op.create_index("ix_billit_companies_environment", "billit_companies", ["environment"])
    op.create_index("ix_billit_companies_vat_number_hash", "billit_companies", ["vat_number_hash"])

    op.create_table(
        "confirmation_challenges",
        sa.Column("challenge_id", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=64), nullable=False),
        sa.Column("client_id", sa.String(length=255), nullable=False),
        sa.Column("connection_id", sa.String(length=64), nullable=False),
        sa.Column("environment", sa.String(length=32), nullable=False),
        sa.Column("company_party_id", sa.Integer(), nullable=False),
        sa.Column("operation_type", sa.String(length=64), nullable=False),
        sa.Column("resource_type", sa.String(length=64), nullable=True),
        sa.Column("resource_id", sa.String(length=255), nullable=True),
        sa.Column("summary_json", sa.JSON(), nullable=False),
        sa.Column("operation_hash", sa.String(length=128), nullable=False),
        sa.Column("required_scope", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("nonce_hash", sa.String(length=128), nullable=False),
        sa.Column("confirmation_token_hash", sa.String(length=128), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["actors.actor_id"]),
        sa.ForeignKeyConstraint(["client_id"], ["oauth_clients.client_id"]),
        sa.ForeignKeyConstraint(["connection_id"], ["billit_connections.connection_id"]),
        sa.PrimaryKeyConstraint("challenge_id"),
        sa.UniqueConstraint("confirmation_token_hash"),
        sa.UniqueConstraint("nonce_hash"),
    )
    op.create_index(
        "ix_confirmation_challenges_actor_id",
        "confirmation_challenges",
        ["actor_id"],
    )
    op.create_index(
        "ix_confirmation_challenges_client_id",
        "confirmation_challenges",
        ["client_id"],
    )
    op.create_index(
        "ix_confirmation_challenges_company_party_id",
        "confirmation_challenges",
        ["company_party_id"],
    )
    op.create_index(
        "ix_confirmation_challenges_expires_at",
        "confirmation_challenges",
        ["expires_at"],
    )
    op.create_index(
        "ix_confirmation_challenges_operation_hash",
        "confirmation_challenges",
        ["operation_hash"],
    )
    op.create_index(
        "ix_confirmation_challenges_operation_type",
        "confirmation_challenges",
        ["operation_type"],
    )
    op.create_index(
        "ix_confirmation_challenges_resource_id",
        "confirmation_challenges",
        ["resource_id"],
    )
    op.create_index(
        "ix_confirmation_challenges_status",
        "confirmation_challenges",
        ["status"],
    )

    op.create_table(
        "idempotency_records",
        sa.Column("idempotency_id", sa.String(length=64), nullable=False),
        sa.Column("idempotency_key_hash", sa.String(length=128), nullable=False),
        sa.Column("connection_id", sa.String(length=64), nullable=False),
        sa.Column("company_party_id", sa.Integer(), nullable=False),
        sa.Column("operation_type", sa.String(length=64), nullable=False),
        sa.Column("operation_hash", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("billit_resource_type", sa.String(length=64), nullable=True),
        sa.Column("billit_resource_id", sa.String(length=255), nullable=True),
        sa.Column("billit_error_code", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["connection_id"], ["billit_connections.connection_id"]),
        sa.PrimaryKeyConstraint("idempotency_id"),
        sa.UniqueConstraint(
            "connection_id",
            "company_party_id",
            "operation_type",
            "idempotency_key_hash",
            name="uq_idempotency_connection_company_operation_key",
        ),
    )
    op.create_index(
        "ix_idempotency_records_billit_resource_id",
        "idempotency_records",
        ["billit_resource_id"],
    )
    op.create_index(
        "ix_idempotency_records_company_party_id",
        "idempotency_records",
        ["company_party_id"],
    )
    op.create_index(
        "ix_idempotency_records_idempotency_key_hash",
        "idempotency_records",
        ["idempotency_key_hash"],
    )
    op.create_index(
        "ix_idempotency_records_operation_hash",
        "idempotency_records",
        ["operation_hash"],
    )
    op.create_index(
        "ix_idempotency_records_operation_type",
        "idempotency_records",
        ["operation_type"],
    )
    op.create_index("ix_idempotency_records_status", "idempotency_records", ["status"])

    op.create_table(
        "audit_events",
        sa.Column("audit_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actor_id", sa.String(length=64), nullable=True),
        sa.Column("client_id", sa.String(length=255), nullable=True),
        sa.Column("connection_id", sa.String(length=64), nullable=True),
        sa.Column("environment", sa.String(length=32), nullable=True),
        sa.Column("company_party_id", sa.Integer(), nullable=True),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("operation_class", sa.String(length=64), nullable=False),
        sa.Column("tool_name", sa.String(length=128), nullable=True),
        sa.Column("resource_refs", sa.JSON(), nullable=False),
        sa.Column("request_hash", sa.String(length=128), nullable=True),
        sa.Column("response_hash", sa.String(length=128), nullable=True),
        sa.Column("summary_json", sa.JSON(), nullable=False),
        sa.Column("outcome", sa.String(length=64), nullable=False),
        sa.Column("error_code", sa.String(length=128), nullable=True),
        sa.Column("correlation_id", sa.String(length=128), nullable=False),
        sa.Column("billit_request_id", sa.String(length=255), nullable=True),
        sa.Column("ip_hash", sa.String(length=128), nullable=True),
        sa.Column("user_agent_hash", sa.String(length=128), nullable=True),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["actor_id"], ["actors.actor_id"]),
        sa.ForeignKeyConstraint(["client_id"], ["oauth_clients.client_id"]),
        sa.PrimaryKeyConstraint("audit_id"),
    )
    op.create_index("ix_audit_actor_created", "audit_events", ["actor_id", "created_at"])
    op.create_index("ix_audit_company_created", "audit_events", ["company_party_id", "created_at"])
    op.create_index("ix_audit_events_actor_id", "audit_events", ["actor_id"])
    op.create_index("ix_audit_events_client_id", "audit_events", ["client_id"])
    op.create_index("ix_audit_events_company_party_id", "audit_events", ["company_party_id"])
    op.create_index("ix_audit_events_connection_id", "audit_events", ["connection_id"])
    op.create_index("ix_audit_events_correlation_id", "audit_events", ["correlation_id"])
    op.create_index("ix_audit_events_environment", "audit_events", ["environment"])
    op.create_index("ix_audit_events_error_code", "audit_events", ["error_code"])
    op.create_index("ix_audit_events_event_type", "audit_events", ["event_type"])
    op.create_index("ix_audit_events_operation_class", "audit_events", ["operation_class"])
    op.create_index("ix_audit_events_outcome", "audit_events", ["outcome"])
    op.create_index("ix_audit_events_tool_name", "audit_events", ["tool_name"])


def downgrade() -> None:
    """Drop hosted OAuth tables introduced by this revision."""

    op.drop_table("audit_events")
    op.drop_table("idempotency_records")
    op.drop_table("confirmation_challenges")
    op.drop_table("billit_companies")
    op.drop_table("billit_oauth_grants")
    op.drop_table("billit_connections")
    op.drop_table("oauth_token_revocations")
    op.drop_table("oauth_auth_codes")
    op.drop_table("oauth_authorization_transactions")
    op.drop_table("oauth_clients")
    op.drop_table("actors")
