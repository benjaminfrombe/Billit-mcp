"""Read-only live canary for the curated local API-key runtime."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

from scripts.local.billit_canary.shared import (
    SANDBOX_KEYCHAIN_SERVICE,
    CanaryClient,
    ReadOnlyBillitClient,
    api_key_header_proof,
    probe_record,
    resolve_canary_settings,
)

from billit.client import BillitAPIClient, BillitSettings
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit_mcp.local_api_key.runtime import LocalAPIKeyRuntime
from billit_mcp.local_api_key.state import LocalStateStore

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


async def run_api_key_canary(
    *,
    base_url: str,
    output_root: Path,
    keychain_reader: Callable[[str], str | None],
    client_factory: Callable[[BillitSettings], CanaryClient] = BillitAPIClient,
    write_override_requested: bool = False,
) -> Path:
    """Run the curated local/private API-key canary path."""

    settings = resolve_canary_settings(base_url, keychain_reader=keychain_reader)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)
    raw_client = client_factory(settings.billit)
    client = ReadOnlyBillitClient(raw_client, allow_writes=False)
    runtime = LocalAPIKeyRuntime(
        settings=settings.billit,
        state=LocalStateStore(output_dir / "local-api-key-state.db"),
        client_factory=lambda _: client,
    )

    probes: list[dict[str, object]] = []
    try:
        account_endpoint = "/account/accountInformation"
        account_resp = await client.request("GET", account_endpoint)
        probes.append(probe_record(account_endpoint, account_resp))

        for endpoint in ["/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT]:
            response = await client.request("GET", endpoint, params=list_params(skip=None, top=5))
            probes.append(probe_record(endpoint, response))

        reports_endpoint = report_endpoint()
        reports_resp = await client.request("GET", reports_endpoint)
        probes.append(probe_record(reports_endpoint, reports_resp))

        connection_status = await runtime.connection_status()
        probes.append(probe_record("curated:billit.connection_status", connection_status))

        list_companies = await runtime.list_companies()
        probes.append(probe_record("curated:billit.list_companies", list_companies))

        search_orders = await runtime.search_orders(
            direction="income", order_type="invoice", limit=5
        )
        probes.append(probe_record("curated:billit.search_orders", search_orders))

        invoice_prepare = await runtime.invoice_prepare(
            customer={"name": "Live canary placeholder"},
            lines=[
                {
                    "description": "Read-only canary line",
                    "quantity": 1,
                    "unit_price": 1,
                    "vat_percentage": 21,
                }
            ],
            order_date=datetime.now(UTC).date().isoformat(),
            expiry_date=(datetime.now(UTC) + timedelta(days=30)).date().isoformat(),
            desired_transport="Peppol",
        )
        probes.append(probe_record("curated:billit.invoice.prepare", invoice_prepare))

        invoice_summary = await runtime.invoice_summary(
            start_date="2000-01-01",
            end_date="2099-12-31",
        )
        probes.append(probe_record("curated:billit.invoice.summary", invoice_summary))

        write_block = await runtime.invoice_create_draft(
            customer={"name": "Live canary write block placeholder"},
            lines=[{"description": "blocked", "quantity": 1, "unit_price": 1}],
            order_date=datetime.now(UTC).date().isoformat(),
            expiry_date=(datetime.now(UTC) + timedelta(days=30)).date().isoformat(),
            idempotency_key="live-canary-write-block",
        )
        probes.append(
            {
                "endpoint": "curated:billit.invoice.create_draft.write_blocked",
                "success": write_block.get("error_code") == "LOCAL_WRITES_DISABLED",
                "error_code": write_block.get("error_code"),
                "item_count": 0,
            }
        )
    finally:
        await runtime.close()

    header_proof = api_key_header_proof(raw_client, settings.billit)
    passed = all(
        [
            any(
                probe["endpoint"] == "/account/accountInformation" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"]
                in {"/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT}
                and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == FINANCIAL_TRANSACTIONS_ENDPOINT and probe["success"]
                for probe in probes
            ),
            any(probe["endpoint"] == report_endpoint() and probe["success"] for probe in probes),
            any(
                probe["endpoint"] == "curated:billit.connection_status" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == "curated:billit.list_companies" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == "curated:billit.search_orders" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == "curated:billit.invoice.prepare" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == "curated:billit.invoice.summary" and probe["success"]
                for probe in probes
            ),
            any(
                probe["endpoint"] == "curated:billit.invoice.create_draft.write_blocked"
                and probe["success"]
                for probe in probes
            ),
            header_proof["api_key_header_present"],
            header_proof["party_id_header_correct"],
            header_proof["context_party_id_header_absent"],
        ]
    )

    report = {
        "timestamp": timestamp,
        "mode": "api-key-readonly",
        "environment": settings.environment,
        "base_url_host": base_url.replace("https://", "").replace("http://", "").split("/")[0],
        "read_only": True,
        "writes_enabled": False,
        "write_override_ignored": write_override_requested,
        "key_source": settings.key_source,
        "keychain_service": SANDBOX_KEYCHAIN_SERVICE,
        "explicit_party_id": True,
        "header_proof": header_proof,
        "local_state_db": "local-api-key-state.db",
        "endpoint_decisions": {
            "financial_transactions": FINANCIAL_TRANSACTIONS_ENDPOINT,
            "reports": report_endpoint(),
        },
        "probes": probes,
        "passed": passed,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if not passed:
        raise SystemExit(f"Live Billit canary failed; sanitized report: {report_path}")
    return report_path
