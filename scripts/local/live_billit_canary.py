"""Local read-only Billit canary with sanitized evidence output."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import platform
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from dotenv import load_dotenv

from billit.client import BillitAPIClient, BillitSettings
from billit.endpoints import FINANCIAL_TRANSACTIONS_ENDPOINT, list_params, report_endpoint
from billit.services.ai_composite import generate_invoice_summary
from billit.smart_search import normalize_items

if TYPE_CHECKING:
    from collections.abc import Callable

SANDBOX_BASE_URL = "https://api.sandbox.billit.be/v1"
SANDBOX_KEYCHAIN_SERVICE = "BILLIT_SANDBOX_API_KEY_K4K"


class CanaryClient(Protocol):
    """Small protocol required by the live canary."""

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]: ...

    async def close(self) -> None: ...


@dataclass(frozen=True)
class CanarySettings:
    """Resolved non-secret canary configuration."""

    billit: BillitSettings
    environment: str
    key_source: str


class ReadOnlyBillitClient:
    """Guard canary probes from accidental writes."""

    def __init__(self, client: CanaryClient, *, allow_writes: bool = False) -> None:
        self._client = client
        self.allow_writes = allow_writes

    async def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        if method.upper() != "GET" and not self.allow_writes:
            return {
                "success": False,
                "data": None,
                "error": f"Canary blocked non-read request: {method.upper()} {url}",
                "error_code": "LIVE_CANARY_WRITE_BLOCKED",
            }
        return await self._client.request(method, url, **kwargs)

    async def close(self) -> None:
        await self._client.close()


def environment_name(base_url: str) -> str:
    """Classify the Billit target environment without exposing credentials."""

    if "sandbox" in base_url:
        return "sandbox"
    if "api.billit.be" in base_url:
        return "production"
    return "custom"


def read_keychain_secret(service: str) -> str | None:
    """Read a macOS Keychain generic-password secret by service name."""

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


def first_present_env(*names: str) -> tuple[str, str] | None:
    """Return the first non-empty environment variable value and its name."""

    for name in names:
        value = os.getenv(name)
        if value:
            return value, name
    return None


def resolve_canary_settings(
    base_url: str,
    *,
    keychain_reader: Callable[[str], str | None] = read_keychain_secret,
) -> CanarySettings:
    """Resolve Billit settings for the canary without mutating process env."""

    environment = environment_name(base_url)
    if environment == "sandbox":
        env_key = first_present_env("BILLIT_SANDBOX_API_KEY_K4K", "BILLIT_SANDBOX_API_KEY")
        if env_key is not None:
            api_key, key_source = env_key
        else:
            keychain_secret = keychain_reader(SANDBOX_KEYCHAIN_SERVICE)
            if keychain_secret:
                api_key = keychain_secret
                key_source = f"keychain:{SANDBOX_KEYCHAIN_SERVICE}"
            else:
                generic_key = first_present_env("BILLIT_API_KEY")
                if generic_key is None:
                    raise SystemExit(
                        "Sandbox canary requires BILLIT_SANDBOX_API_KEY_K4K, "
                        f"BILLIT_SANDBOX_API_KEY, Keychain service {SANDBOX_KEYCHAIN_SERVICE}, "
                        "or BILLIT_API_KEY."
                    )
                api_key, key_source = generic_key
        party_id = os.getenv("BILLIT_SANDBOX_PARTY_ID") or os.getenv("BILLIT_PARTY_ID")
    else:
        generic_key = first_present_env("BILLIT_API_KEY")
        if generic_key is None:
            raise SystemExit("Non-sandbox canary requires BILLIT_API_KEY.")
        api_key, key_source = generic_key
        party_id = os.getenv("BILLIT_PARTY_ID")

    if not party_id:
        raise SystemExit("BILLIT_PARTY_ID is required for the live Billit canary.")

    return CanarySettings(
        billit=BillitSettings(
            base_url=base_url,
            api_key=api_key,
            party_id=party_id,
            context_party_id=os.getenv("BILLIT_CONTEXT_PARTY_ID"),
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "50")),
        ),
        environment=environment,
        key_source=key_source,
    )


def count_items(data: Any) -> int:
    """Return a sanitized count for arbitrary Billit payloads."""

    items = normalize_items(data)
    if items:
        return len(items)
    if isinstance(data, dict):
        return len(data)
    if isinstance(data, list):
        return len(data)
    return 0


def probe_record(endpoint: str, response: dict[str, Any]) -> dict[str, Any]:
    """Return sanitized probe evidence."""

    return {
        "endpoint": endpoint,
        "success": bool(response.get("success")),
        "error_code": response.get("error_code"),
        "item_count": count_items(response.get("data")),
    }


async def run_canary(
    *,
    base_url: str = SANDBOX_BASE_URL,
    output_root: Path = Path(".local/billit-live-canary"),
    allow_writes: bool = False,
    keychain_reader: Callable[[str], str | None] = read_keychain_secret,
    client_factory: Callable[[BillitSettings], CanaryClient] = BillitAPIClient,
) -> Path:
    """Run the local live Billit canary and return the sanitized report path."""

    settings = resolve_canary_settings(base_url, keychain_reader=keychain_reader)
    raw_client = client_factory(settings.billit)
    client = ReadOnlyBillitClient(raw_client, allow_writes=allow_writes)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_dir = output_root / timestamp
    output_dir.mkdir(parents=True, exist_ok=False)

    probes: list[dict[str, Any]] = []
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

        composite_resp = await generate_invoice_summary(client, "2000-01-01", "2099-12-31")
        probes.append(probe_record("composite:generate_invoice_summary", composite_resp))
    finally:
        await client.close()

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
                probe["endpoint"] == "composite:generate_invoice_summary" and probe["success"]
                for probe in probes
            ),
        ]
    )

    report = {
        "timestamp": timestamp,
        "environment": settings.environment,
        "base_url_host": base_url.replace("https://", "").replace("http://", "").split("/")[0],
        "read_only": True,
        "writes_enabled": allow_writes,
        "key_source": settings.key_source,
        "keychain_service": SANDBOX_KEYCHAIN_SERVICE,
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
        default=Path(".local/billit-live-canary"),
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

    allow_writes = os.getenv("BILLIT_LIVE_CANARY_ALLOW_WRITES") == "1"
    report_path = asyncio.run(
        run_canary(
            base_url=args.base_url,
            output_root=args.output_root,
            allow_writes=allow_writes,
        )
    )
    print(f"Live Billit canary passed; sanitized report: {report_path}")


if __name__ == "__main__":
    main()
