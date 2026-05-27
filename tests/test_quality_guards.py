"""Maintainability guardrails for Billit MCP runtime source shape."""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_runtime_and_canary_files_stay_below_review_size_threshold() -> None:
    """New runtime/canary source files should stay reviewable."""

    root = Path(__file__).resolve().parents[1]
    paths = [
        *sorted((root / "src/billit_mcp/local_api_key").glob("*.py")),
        *sorted((root / "src/billit_mcp/hosted_tools").glob("*.py")),
        *sorted((root / "src/billit_mcp/services").glob("hosted_*.py")),
        root / "src/billit_mcp/services/invoice_workflow.py",
        root / "scripts/local/live_billit_canary.py",
        *sorted((root / "scripts/local/billit_canary").glob("*.py")),
    ]

    line_counts = {
        path.relative_to(root).as_posix(): sum(1 for _ in path.open())
        for path in paths
        if path.name != "__init__.py"
    }
    oversized = {path: lines for path, lines in line_counts.items() if lines > 800}

    assert oversized == {}


def test_tracked_root_markdown_does_not_collect_implementation_plans() -> None:
    """Tracked implementation plans belong under docs, not the repository root."""

    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["git", "ls-files", "*.md", "*.MD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )

    forbidden = []
    for tracked in result.stdout.splitlines():
        path = Path(tracked)
        if len(path.parts) != 1:
            continue
        name = path.name.lower()
        if "goal-prompt" in name or name.endswith("-plan.md"):
            forbidden.append(tracked)

    assert forbidden == []
