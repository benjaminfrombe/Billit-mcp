"""Local read-only Billit canary with sanitized evidence output."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from billit.client import BillitAPIClient
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, report_endpoint
from billit.services.ai_composite import generate_invoice_summary
from billit.smart_search import normalize_items

SANDBOX_BASE_URL = "https://api.sandbox.billit.be/v1"
KEYCHAIN_SERVICE = "BILLIT_SANDBOX_API_KEY_K4K"


def _env_name(base_url: str) -> str:
    if "sandbox" in base_url:
        return "sandbox"
    if "api.billit.be" in base_url:
        return "production"
    return "custom"


def _read_keychain_secret(service: str) -> str | None:
    if platform.system() != "Darwin":
        return None
    result = subprocess.run(
        ["security", "find-generic-password", "-w", "-s", service],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    secret = result.stdout.strip()
    return secret or None


def _configure_environment(base_url: str) -> None:
    os.environ["BILLIT_BASE_URL"] = base_url
    if _env_name(base_url) == "sandbox":
        sandbox_key = os.getenv("BILLIT_SANDBOX_API_KEY") or _read_keychain_secret(KEYCHAIN_SERVICE)
        if sandbox_key:
            os.environ["BILLIT_API_KEY"] = sandbox_key
        if os.getenv("BILLIT_SANDBOX_PARTY_ID"):
            os.environ["BILLIT_PARTY_ID"] = os.environ["BILLIT_SANDBOX_PARTY_ID"]
    elif not os.getenv("BILLIT_API_KEY"):
        keychain_secret = _read_keychain_secret(KEYCHAIN_SERVICE)
        if keychain_secret:
            os.environ["BILLIT_API_KEY"] = keychain_secret
    if not os.getenv("BILLIT_PARTY_ID"):
        raise SystemExit("BILLIT_PARTY_ID is required for the live Billit canary.")
    if not os.getenv("BILLIT_API_KEY"):
        raise SystemExit(
            "BILLIT_API_KEY is required. Set it in env/.env or store it in macOS "
            f"Keychain service {KEYCHAIN_SERVICE}."
        )


def _count_items(data: Any) -> int:
    items = normalize_items(data)
    if items:
        return len(items)
    if isinstance(data, dict):
        return len(data)
    if isinstance(data, list):
        return len(data)
    return 0


def _probe_record(endpoint: str, response: dict[str, Any]) -> dict[str, Any]:
    return {
        "endpoint": endpoint,
        "success": bool(response.get("success")),
        "error_code": response.get("error_code"),
        "item_count": _count_items(response.get("data")),
    }


async def _run_canary(base_url: str, output_root: Path) -> Path:
    client = BillitAPIClient()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)

    probes: list[dict[str, Any]] = []
    try:
        account_endpoint = "/account/accountInformation"
        account_resp = await client.request("GET", account_endpoint)
        probes.append(_probe_record(account_endpoint, account_resp))

        for endpoint in ["/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT]:
            resp = await client.request("GET", endpoint, params={"$top": 5})
            probes.append(_probe_record(endpoint, resp))

        report_path = report_endpoint()
        report_resp = await client.request("GET", report_path)
        probes.append(_probe_record(report_path, report_resp))

        composite_resp = await generate_invoice_summary(client, "2000-01-01", "2099-12-31")
        probes.append(_probe_record("composite:generate_invoice_summary", composite_resp))
    finally:
        await client.close()

    auth_success = any(
        probe["endpoint"] == "/account/accountInformation" and probe["success"] for probe in probes
    )
    collection_success = any(
        probe["endpoint"] in {"/parties", "/orders", "/products", FINANCIAL_TRANSACTIONS_ENDPOINT}
        and probe["success"]
        for probe in probes
    )
    financial_success = any(
        probe["endpoint"] == FINANCIAL_TRANSACTIONS_ENDPOINT and probe["success"]
        for probe in probes
    )
    report_success = any(
        probe["endpoint"] == report_endpoint() and probe["success"] for probe in probes
    )
    composite_success = any(
        probe["endpoint"] == "composite:generate_invoice_summary" and probe["success"]
        for probe in probes
    )
    passed = all(
        [auth_success, collection_success, financial_success, report_success, composite_success]
    )

    report = {
        "timestamp": timestamp,
        "environment": _env_name(base_url),
        "base_url_host": base_url.replace("https://", "").replace("http://", "").split("/")[0],
        "read_only": True,
        "writes_enabled": os.getenv("BILLIT_LIVE_CANARY_ALLOW_WRITES") == "1",
        "keychain_service": KEYCHAIN_SERVICE,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--read-only",
        action="store_true",
        help="Required acknowledgement that this canary will not perform writes.",
    )
    parser.add_argument(
        "--base-url",
        default=SANDBOX_BASE_URL,
        help="Billit API base URL. Defaults to sandbox.",
    )
    parser.add_argument(
        "--output-root",
        default=".local/billit-live-canary",
        type=Path,
        help="Directory for sanitized canary evidence.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    if os.getenv("CI"):
        raise SystemExit("Refusing to run the live Billit canary in CI.")
    if not args.read_only:
        raise SystemExit("Pass --read-only to acknowledge that no write probes will run.")
    if args.base_url != SANDBOX_BASE_URL and os.getenv("BILLIT_LIVE_CANARY_ENV") != "production":
        raise SystemExit(
            "Non-sandbox canary runs require BILLIT_LIVE_CANARY_ENV=production "
            "and still remain read-only."
        )

    _configure_environment(args.base_url)
    report_path = asyncio.run(_run_canary(args.base_url, args.output_root))
    print(f"Live Billit canary passed; sanitized report: {report_path}")


if __name__ == "__main__":
    main()
