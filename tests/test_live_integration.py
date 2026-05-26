"""Read-only live Billit canary pytest wrapper.

Run with:
    uv run pytest tests/test_live_integration.py -q --live
"""

from __future__ import annotations

import json

import pytest
from scripts.local.live_billit_canary import SANDBOX_BASE_URL, run_canary

pytestmark = pytest.mark.live


@pytest.mark.asyncio
async def test_live_billit_read_only_canary(tmp_path) -> None:
    """Run the same read-only canary used for local endpoint drift evidence."""

    report_path = await run_canary(base_url=SANDBOX_BASE_URL, output_root=tmp_path)

    report = json.loads(report_path.read_text())
    assert report["passed"] is True
    assert report["read_only"] is True
    assert report["writes_enabled"] is False
