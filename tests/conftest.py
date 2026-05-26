"""
Pytest configuration for Billit MCP tests.
"""
import pytest


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Run live integration tests against actual API"
    )


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "live: mark test as requiring live API access"
    )


def pytest_collection_modifyitems(config, items):
    """Skip live tests unless --live flag is provided."""
    if not config.getoption("--live"):
        skip_live = pytest.mark.skip(reason="need --live option to run")
        for item in items:
            if "live" in item.keywords or "test_live_integration" in str(item.fspath):
                item.add_marker(skip_live)