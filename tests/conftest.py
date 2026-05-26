"""
Pytest configuration for Billit MCP tests.
"""

from collections.abc import Iterator

import pytest

from billit.client import BillitAPIClient


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Run live integration tests against actual API",
    )


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "live: mark test as requiring live API access")
    config.addinivalue_line(
        "markers",
        "allow_billit_request: test intentionally exercises BillitAPIClient.request with mocks",
    )


def pytest_collection_modifyitems(config, items):
    """Skip live tests unless --live flag is provided."""
    if not config.getoption("--live"):
        skip_live = pytest.mark.skip(reason="need --live option to run")
        for item in items:
            if "live" in item.keywords or "test_live_integration" in str(item.fspath):
                item.add_marker(skip_live)


@pytest.fixture(autouse=True)
def billit_test_environment(
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    """Provide fake Billit configuration for non-live tests."""

    if request.config.getoption("--live"):
        return
    monkeypatch.setenv("BILLIT_API_KEY", "test-api-key")
    monkeypatch.setenv("BILLIT_BASE_URL", "http://test.invalid")
    monkeypatch.setenv("BILLIT_PARTY_ID", "1")
    monkeypatch.setenv("BILLIT_CONTEXT_PARTY_ID", "")
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "100000")


@pytest.fixture(autouse=True)
def forbid_unmocked_billit_requests(
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> Iterator[None]:
    """Fail normal tests that forget to mock the shared Billit client."""

    if (
        request.config.getoption("--live")
        or request.node.get_closest_marker("live")
        or request.node.get_closest_marker("allow_billit_request")
    ):
        yield
        return

    async def _refuse_request(
        self: BillitAPIClient,
        method: str,
        url: str,
        **kwargs: object,
    ) -> dict[str, object]:
        raise AssertionError(
            "Unexpected BillitAPIClient.request in non-live test. "
            "Mock this method in the test or run with --live for real Billit access."
        )

    monkeypatch.setattr(BillitAPIClient, "request", _refuse_request)
    yield
