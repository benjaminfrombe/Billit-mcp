"""Maintainability guardrails for Billit MCP runtime source shape."""

from __future__ import annotations

from pathlib import Path


def test_runtime_and_canary_files_stay_below_review_size_threshold() -> None:
    """New runtime/canary source files should stay reviewable."""

    root = Path(__file__).resolve().parents[1]
    paths = [
        *sorted((root / "src/billit_mcp/local_api_key").glob("*.py")),
        *sorted((root / "src/billit_mcp/hosted_tools").glob("*.py")),
        root / "src/billit_mcp/services/hosted_runtime.py",
        root / "src/billit_mcp/services/invoice_workflow.py",
        root / "scripts/local/live_billit_canary.py",
        *sorted((root / "scripts/local/billit_canary").glob("*.py")),
    ]

    oversized = {
        path.relative_to(root).as_posix(): sum(1 for _ in path.open())
        for path in paths
        if path.name != "__init__.py" and sum(1 for _ in path.open()) > 1_000
    }

    assert oversized == {}
