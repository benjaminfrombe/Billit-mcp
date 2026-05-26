"""Local read-only Billit canary with sanitized evidence output."""

from __future__ import annotations

import argparse
import asyncio
import os
from pathlib import Path
from typing import TYPE_CHECKING

from dotenv import load_dotenv
from scripts.local.billit_canary.api_key import run_api_key_canary
from scripts.local.billit_canary.shared import (
    SANDBOX_BASE_URL,
    SANDBOX_KEYCHAIN_SERVICE,
    CanaryClient,
    CanarySettings,
    ReadOnlyBillitClient,
    api_key_header_proof,
    count_items,
    environment_name,
    first_present_env,
    probe_record,
    read_keychain_secret,
    resolve_canary_party_id,
    resolve_canary_settings,
)

from billit.client import BillitAPIClient, BillitSettings

if TYPE_CHECKING:
    from collections.abc import Callable


async def run_canary(
    *,
    base_url: str = SANDBOX_BASE_URL,
    output_root: Path = Path(".local/billit-live-canary"),
    allow_writes: bool = False,
    mode: str = "api-key-readonly",
    keychain_reader: Callable[[str], str | None] = read_keychain_secret,
    client_factory: Callable[[BillitSettings], CanaryClient] = BillitAPIClient,
) -> Path:
    """Run the selected local live Billit canary mode."""

    if mode == "api-key-readonly":
        return await run_api_key_canary(
            base_url=base_url,
            output_root=output_root,
            keychain_reader=keychain_reader,
            client_factory=client_factory,
            write_override_requested=allow_writes,
        )
    if mode == "hosted-oauth-readonly":
        from scripts.local.billit_canary.hosted_oauth import run_hosted_oauth_canary

        return await run_hosted_oauth_canary(
            base_url=base_url,
            output_root=output_root,
            write_override_requested=allow_writes,
        )
    raise SystemExit(f"Unsupported live canary mode: {mode}")


async def ensure_hosted_canary_schema(database_url: str) -> str:
    """Run or stamp hosted canary migrations without importing hosted code at startup."""

    from scripts.local.billit_canary.hosted_oauth import ensure_hosted_canary_schema as impl

    return await impl(database_url)


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
    parser.add_argument(
        "--mode",
        choices=["api-key-readonly", "hosted-oauth-readonly"],
        default="api-key-readonly",
        help="Canary mode. Hosted mode requires a pre-seeded sandbox OAuth grant.",
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

    report_path = asyncio.run(
        run_canary(
            base_url=args.base_url,
            output_root=args.output_root,
            allow_writes=os.getenv("BILLIT_LIVE_CANARY_ALLOW_WRITES") == "1",
            mode=args.mode,
        )
    )
    print(f"Live Billit canary passed; sanitized report: {report_path}")


__all__ = [
    "SANDBOX_BASE_URL",
    "SANDBOX_KEYCHAIN_SERVICE",
    "CanaryClient",
    "CanarySettings",
    "ReadOnlyBillitClient",
    "api_key_header_proof",
    "count_items",
    "ensure_hosted_canary_schema",
    "environment_name",
    "first_present_env",
    "probe_record",
    "read_keychain_secret",
    "resolve_canary_party_id",
    "resolve_canary_settings",
    "run_canary",
]


if __name__ == "__main__":
    main()
