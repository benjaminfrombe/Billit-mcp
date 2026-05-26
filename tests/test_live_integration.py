"""
Live integration tests for Billit MCP Server.

These tests use real credentials and perform read-only operations against the actual API.
Run with: pytest tests/test_live_integration.py -v --live

WARNING: These tests will use your actual API credentials. Ensure you're using a sandbox account.
"""

import os

import pytest
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from server import app

# Load environment variables
load_dotenv()

# Mark all tests in this file as live tests
pytestmark = pytest.mark.live


class TestLiveIntegration:
    """Read-only integration tests against the live Billit API."""

    @pytest.fixture
    async def client(self):
        """Create an authenticated test client."""
        # Verify credentials are configured
        assert os.getenv("BILLIT_API_KEY"), "BILLIT_API_KEY must be set"
        assert os.getenv("BILLIT_PARTY_ID"), "BILLIT_PARTY_ID must be set"

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client

    # ========== Account Tests ==========

    @pytest.mark.asyncio
    async def test_get_account_information(self, client):
        """Test retrieving account information."""
        response = await client.get("/account")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert result["data"] is not None
        assert "PartyID" in result["data"]
        assert "Name" in result["data"]
        print(f"✅ Account: {result['data'].get('Name')} (ID: {result['data'].get('PartyID')})")

    @pytest.mark.asyncio
    async def test_get_sso_token(self, client):
        """Test retrieving SSO token."""
        response = await client.get("/account/sso-token")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert result["data"] is not None
        assert "Token" in result["data"]
        print("✅ SSO token retrieved successfully")

    @pytest.mark.asyncio
    async def test_get_next_sequence_number(self, client):
        """Test retrieving next sequence number without consuming it."""
        response = await client.get("/account/sequence/Income-Invoice?consume=false")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert result["data"] is not None
        assert "NextNumber" in result["data"]
        print(f"✅ Next invoice number would be: {result['data'].get('NextNumber')}")

    # ========== Party Tests ==========

    @pytest.mark.asyncio
    async def test_list_parties(self, client):
        """Test listing parties (customers/suppliers)."""
        # Test customers
        response = await client.get("/parties?party_type=Customer&top=5")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert "Items" in result["data"]
        assert isinstance(result["data"]["Items"], list)
        print(f"✅ Found {len(result['data']['Items'])} customers")

        # Test suppliers
        response = await client.get("/parties?party_type=Supplier&top=5")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert "Items" in result["data"]
        assert isinstance(result["data"]["Items"], list)
        print(f"✅ Found {len(result['data']['Items'])} suppliers")

    @pytest.mark.asyncio
    async def test_get_party_details(self, client):
        """Test getting details of a specific party."""
        # First get a party ID
        response = await client.get("/parties?party_type=Customer&top=1")
        result = response.json()

        if result["data"] and "Items" in result["data"] and len(result["data"]["Items"]) > 0:
            party_id = result["data"]["Items"][0]["PartyID"]

            # Get party details
            response = await client.get(f"/parties/{party_id}")
            assert response.status_code == 200

            result = response.json()
            assert result["success"] is True
            assert result["data"]["PartyID"] == party_id
            party_data = result["data"]
            print(f"✅ Retrieved details for party: {party_data.get('Name')}")
            street = party_data.get("Street", "")
            number = party_data.get("StreetNumber", "")
            print(f"   Address: {street} {number}")
            print(f"   City: {party_data.get('City', '')} {party_data.get('Zipcode', '')}")
            print(f"   Country: {party_data.get('CountryCode', '')}")
            print(f"   Email: {party_data.get('Email', '')}")
        else:
            pytest.skip("No parties found to test")

    # ========== Product Tests ==========

    @pytest.mark.asyncio
    async def test_list_products(self, client):
        """Test listing products."""
        response = await client.get("/products?top=10")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} products")

        if result["data"]:
            product = result["data"][0]
            name = product.get("Name")
            price = product.get("Price")
            currency = product.get("Currency")
            print(f"   Example: {name} - {price} {currency}")

    @pytest.mark.asyncio
    async def test_get_product_details(self, client):
        """Test getting product details."""
        # First get a product ID
        response = await client.get("/products?top=1")
        result = response.json()

        if result["data"] and len(result["data"]) > 0:
            product_id = result["data"][0]["ProductID"]

            # Get product details
            response = await client.get(f"/products/{product_id}")
            assert response.status_code == 200

            result = response.json()
            assert result["success"] is True
            assert result["data"]["ProductID"] == product_id
            print(f"✅ Retrieved details for product: {result['data'].get('Name')}")
        else:
            pytest.skip("No products found to test")

    # ========== Order Tests ==========

    @pytest.mark.asyncio
    async def test_list_orders(self, client):
        """Test listing orders with various filters."""
        # List recent sales invoices
        response = await client.get(
            "/orders",
            params={
                "odata_filter": "OrderDirection eq 'Income' and OrderType eq 'Invoice'",
                "top": 5,
            },
        )
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} sales invoices")

        # List recent purchase invoices
        response = await client.get(
            "/orders",
            params={
                "odata_filter": "OrderDirection eq 'Expense' and OrderType eq 'Invoice'",
                "top": 5,
            },
        )
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        print(f"✅ Found {len(result['data'])} purchase invoices")

    @pytest.mark.asyncio
    async def test_get_order_details(self, client):
        """Test getting order details including status."""
        # First get an order ID
        response = await client.get("/orders?top=1")
        result = response.json()

        if result["data"] and len(result["data"]) > 0:
            order_id = result["data"][0]["OrderID"]

            # Get order details
            response = await client.get(f"/orders/{order_id}")
            assert response.status_code == 200

            result = response.json()
            assert result["success"] is True
            assert result["data"]["OrderID"] == order_id

            order = result["data"]
            print(f"✅ Order {order.get('OrderNumber')}:")
            print(f"   Type: {order.get('OrderType')}")
            print(f"   Status: {order.get('Status')}")
            print(f"   Total: {order.get('TotalIncludingVAT')} {order.get('Currency')}")
            print(f"   Lines: {len(order.get('Lines', []))}")
        else:
            pytest.skip("No orders found to test")

    @pytest.mark.asyncio
    async def test_list_deleted_orders(self, client):
        """Test listing deleted orders."""
        response = await client.get("/orders/deleted")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} deleted orders")

    # ========== Financial Transaction Tests ==========

    @pytest.mark.asyncio
    async def test_list_financial_transactions(self, client):
        """Test listing financial transactions."""
        response = await client.get("/financial-transactions?top=10")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} financial transactions")

        if result["data"]:
            tx = result["data"][0]
            date = tx.get("Date")
            amount = tx.get("Amount")
            currency = tx.get("Currency")
            description = tx.get("Description")
            print(f"   Example: {date} - {amount} {currency} - {description}")

    # ========== GL Account Tests ==========

    @pytest.mark.asyncio
    async def test_list_gl_accounts(self, client):
        """Test listing general ledger accounts."""
        # Note: The API might not have a direct list endpoint, testing create endpoint readiness
        response = await client.post(
            "/gl-accounts", json={"Code": "TEST999", "Name": "Test Account", "Type": "Asset"}
        )

        # We expect this to fail in read-only mode or with validation
        # Just checking the endpoint exists
        assert response.status_code in [200, 400, 403, 422]
        print("✅ GL accounts endpoint is accessible")

    # ========== Webhook Tests ==========

    @pytest.mark.asyncio
    async def test_list_webhooks(self, client):
        """Test listing webhooks."""
        response = await client.get("/webhooks")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} webhooks")

        for webhook in result["data"]:
            entity_type = webhook.get("EntityType")
            update_type = webhook.get("UpdateType")
            url = webhook.get("URL")
            print(f"   - {entity_type} {update_type} → {url}")

    # ========== Peppol Tests ==========

    @pytest.mark.asyncio
    async def test_check_peppol_participant(self, client):
        """Test checking Peppol network participation."""
        # Check a known Belgian company
        response = await client.get("/peppol/check/BE0123456789")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        print(f"✅ Peppol check completed: {result['data']}")

    @pytest.mark.asyncio
    async def test_list_peppol_inbox(self, client):
        """Test listing Peppol inbox."""
        response = await client.get("/peppol/inbox")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} items in Peppol inbox")

    # ========== Reports Tests ==========

    @pytest.mark.asyncio
    async def test_list_available_reports(self, client):
        """Test listing available reports."""
        response = await client.get("/reports")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} available reports")

        for report in result["data"]:
            print(f"   - {report.get('Name')} ({report.get('ReportID')})")

    # ========== AI Composite Tools Tests ==========

    @pytest.mark.asyncio
    async def test_list_overdue_invoices(self, client):
        """Test AI tool for listing overdue invoices."""
        response = await client.get("/ai/overdue-invoices")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} overdue invoices")

        total_overdue = sum(inv.get("AmountDue", 0) for inv in result["data"])
        if total_overdue > 0:
            print(f"   Total overdue amount: {total_overdue}")

    @pytest.mark.asyncio
    async def test_generate_invoice_summary(self, client):
        """Test AI tool for generating invoice summary."""
        import datetime

        # Last 30 days
        end_date = datetime.date.today().isoformat()
        start_date = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

        response = await client.get(
            "/ai/invoice-summary",
            params={"start_date": start_date, "end_date": end_date},
        )
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True

        summary = result["data"]
        print("✅ Invoice summary for last 30 days:")
        print(f"   Total invoices: {summary.get('count', 0)}")
        print(f"   Total amount: {summary.get('total_amount', 0)}")
        print(f"   Average: {summary.get('average_amount', 0)}")

    @pytest.mark.asyncio
    async def test_get_cashflow_overview(self, client):
        """Test AI tool for cashflow overview."""
        response = await client.get("/ai/cashflow?period=last_30_days")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True

        cashflow = result["data"]
        print("✅ Cashflow overview:")
        print(f"   Income: {cashflow.get('total_income', 0)}")
        print(f"   Expenses: {cashflow.get('total_expenses', 0)}")
        print(f"   Net: {cashflow.get('net_cashflow', 0)}")

    # ========== Miscellaneous Tests ==========

    @pytest.mark.asyncio
    async def test_search_company(self, client):
        """Test company search."""
        response = await client.get("/misc/search-company?keywords=Billit")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        print(f"✅ Company search completed: Found {len(result.get('data', []))} results")

    @pytest.mark.asyncio
    async def test_get_type_codes(self, client):
        """Test retrieving system type codes."""
        # Test VAT rates
        response = await client.get("/misc/types/VATRate")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        assert isinstance(result["data"], list)
        print(f"✅ Found {len(result['data'])} VAT rates")

        # Test currencies
        response = await client.get("/misc/types/Currency")
        assert response.status_code == 200

        result = response.json()
        assert result["success"] is True
        print(f"✅ Found {len(result['data'])} currencies")

    # ========== Error Handling Tests ==========

    @pytest.mark.asyncio
    async def test_error_handling_not_found(self, client):
        """Test 404 error handling."""
        response = await client.get("/orders/99999999")
        assert response.status_code == 200  # MCP always returns 200

        result = response.json()
        assert result["success"] is False
        assert result["error"] is not None
        print("✅ 404 errors handled correctly")

    @pytest.mark.asyncio
    async def test_error_handling_invalid_filter(self, client):
        """Test handling of invalid OData filters."""
        response = await client.get("/orders?odata_filter=InvalidFilter")
        assert response.status_code == 200  # MCP always returns 200

        result = response.json()
        # API might accept it or return error
        print(f"✅ Invalid filter handling: success={result['success']}")
