Of course. Here is a complete, rewritten implementation plan that synthesizes all provided documentation and previous plans into a single, comprehensive guide. This plan is designed to be a definitive, developer-ready document, leaving no tools or key concepts out.

***

### **Implementation Plan: Billit API MCP Server**

#### **1. Executive Overview**

*   **Project Goal:** To build a production-grade, Python-based Model Context Protocol (MCP) server using the FastAPI framework. This server will act as an intelligent middleware, exposing the entire Billit REST API as a secure, standardized, and AI-friendly toolset. It will serve a React-based front end and enable sophisticated financial automation via AI agents.

*   **Key Deliverables:**
    1.  A functional MCP server exposing **66 standardized tools** covering all **15 core Billit API domains**.
    2.  A suite of high-level, AI-oriented tools for complex tasks like reconciliation and summarization.
    3.  A comprehensive testing suite to ensure reliability and correctness.
    4.  Complete developer documentation, including tool specifications and setup instructions.
    5.  A production-ready `Dockerfile` for easy deployment via Uvicorn.

*   **Success Criteria:**
    *   **Functional:** 100% of the 66 defined tools are operational and validated against the Billit sandbox.
    *   **Quality:** >80% unit test coverage; no critical bugs identified in core workflows.
    *   **Performance:** p95 latency under 250ms for non-file-based API calls.
    *   **Security:** No hardcoded secrets; all sensitive data loaded from the environment.

---

#### **2. Architecture & Technology**

**2.1. System Architecture**

The MCP server abstracts the Billit API's complexity, providing a clean, consistent interface.

```
┌──────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ React Client / │─────▶│   MCP Server    │─────▶│   Billit API    │
│   AI Agents    │      │ (FastAPI/Uvicorn) │      │   (REST/JSON)   │
└──────────────┘      └─────────────────┘      └─────────────────┘
```

**2.2. Standard Response Envelope**

To ensure predictable responses, every tool will return a standardized JSON object:

```json
{
  "success": true, // or false
  "data": { ... }, // The tool's successful output, or null on error
  "error": "A human-readable error message if success is false, else null",
  "error_code": "A machine-readable error code (e.g., 'INVALID_VAT_NUMBER'), or null"
}
```

**2.3. Technology Stack**

*   **Language:** Python 3.11+
*   **Web Framework:** FastAPI
*   **HTTP Client:** `httpx` (for asynchronous requests to the Billit API)
*   **Data Validation:** Pydantic v2
*   **Testing:** `pytest`, `pytest-asyncio`, `respx` (for mocking HTTP requests)
*   **Deployment:** Uvicorn

---

#### **3. Getting Started: Developer Setup**

**3.1. Prerequisites**

1.  **Billit Production Account:** Register an account at `https://my.billit.be/Account/Register`.
2.  **API Key & Party ID:**
    *   **API Key:** Find this in your sandbox account under `Profile > Users & API Key`.
    *   **Party ID:** This is your company's unique ID. Find it in the URL when you navigate to `My Company` (e.g., `.../Company/Edit/12345`).
3.  **Development Tools:**
    *   Python 3.11+
    *   Poetry (or `pip`)
    *   Git

**3.2. Initial Setup**

1.  **Clone the Repository & Install Dependencies:**
    ```bash
    git clone <repository-url> && cd billit-mcp-server
    poetry install
    ```
2.  **Configure Environment:**
    Create a `.env` file in the project root. **This file must not be committed to Git.**
    ```ini
    # .env
    # --- Billit API Credentials ---
    BILLIT_API_KEY="YOUR_SANDBOX_API_KEY"
    BILLIT_BASE_URL="https://api.billit.be/v1"
    BILLIT_PARTY_ID="YOUR_COMPANY_ID"
    BILLIT_CONTEXT_PARTY_ID="" # Optional: For accountant use cases

    # --- Server Configuration ---
    MCP_SERVER_PORT=8000
    LOG_LEVEL="INFO"

    # --- Application Settings ---
    RATE_LIMIT_PER_MINUTE=50 # Conservative limit for sandbox
    ```
3.  **Run the Server:**
    ```bash
    poetry run uvicorn server:app --reload
    ```
    The server will be available at `http://localhost:8000`. The interactive API documentation (Swagger UI) will be at `http://localhost:8000/docs`.

---

#### **4. Complete Tool Implementation Plan**

This section details every tool to be implemented, grouped by the Billit API domain.

**4.1. Domain: Party (Contacts) - 4 Tools**
*Docs: [Identifiers](billit_docs_markdown/identifiers.md), [Where can I find my CompanyID or a PartyID](billit_docs_markdown/where-can-i-find-my-companyid-or-a-partyid.md)*

*   `list_parties(party_type: str, odata_filter: str = None, skip: int = 0, top: int = 120)`: Retrieves a paginated list of parties, filtered by `PartyType` ('Customer' or 'Supplier') and optional OData queries.
*   `create_party(party_data: PartyCreate)`: Creates a new customer or supplier.
*   `get_party(party_id: int)`: Retrieves the full details of a single party by its ID.
*   `update_party(party_id: int, party_updates: PartyUpdate)`: Updates an existing party's details using `PATCH`.

**4.2. Domain: Order (Invoices, Credit Notes, etc.) - 9 Tools**
*Docs: [Creating Sales Invoices](billit_docs_markdown/creating-sales-invoices.md), [Retrieve list of invoices](billit_docs_markdown/retrieve-list-of-invoices.md), [Get Information About 1 Invoice/CreditNote](billit_docs_markdown/get-information-about-1-invoice-creditnote.md), [Patchable Properties](billit_docs_markdown/patchable-properties.md)*

*   `list_orders(odata_filter: str = None, skip: int = 0, top: int = 120)`: Retrieves a paginated list of all orders (invoices, credit notes, etc.) with OData filtering.
*   `create_order(order_data: OrderCreate)`: Creates a new order. Billit automatically handles customer creation if the customer doesn't exist.
*   `get_order(order_id: int)`: Retrieves the full details of a specific order, including status, line items, and file attachments.
*   `update_order(order_id: int, order_updates: OrderUpdate)`: Updates patchable properties of an existing order (e.g., `Paid`, `PaidDate`, `IsSent`).
*   `delete_order(order_id: int)`: Deletes a draft order.
*   `record_payment(order_id: int, payment_info: PaymentInfo)`: Records a payment against an order.
*   `send_order(order_ids: List[int], transport_type: str, strict_transport: bool = False)`: Sends one or more orders via a specified transport method (e.g., 'Peppol', 'Email'). The `strict_transport` flag prevents fallback to email if the primary method fails.
*   `add_booking_entries(order_id: int, entries: List[BookingEntry])`: Attaches accounting entries to an order.
*   `list_deleted_orders()`: Retrieves a list of recently deleted orders for synchronization purposes.

**4.3. Domain: FinancialTransaction (Bank Transactions) - 3 Tools**
*Docs: [API For Receiving Supplier Invoices](billit_docs_markdown/api-for-receiving-supplier-invoices.md)*

*   `list_financial_transactions(odata_filter: str = None, skip: int = 0, top: int = 120)`: Retrieves a list of imported bank transactions.
*   `import_transactions_file(file_path: str)`: Imports a bank statement file (e.g., CODA, CSV) by uploading it.
*   `confirm_transaction_import(import_id: str)`: Finalizes a file import process if required by the API.

**4.4. Domain: Product - 3 Tools**

*   `list_products(odata_filter: str = None, skip: int = 0, top: int = 120)`: Retrieves a list of all defined products/services.
*   `get_product(product_id: int)`: Retrieves details of a specific product.
*   `upsert_product(product_data: ProductUpsert)`: Creates a new product or updates an existing one if an ID is provided.

**4.5. Domain: Account - 4 Tools**
*Docs: [Authentication](billit_docs_markdown/authentication.md), [Set Invoice Number - How can I retrieve the next sequence](billit_docs_markdown/set-invoice-number-how-can-i-retrieve-the-next-sequence.md)*

*   `get_account_information()`: Retrieves details about the authenticated account.
*   `get_sso_token()`: Retrieves a Single Sign-On token for logging into the Billit web UI.
*   `get_next_sequence_number(sequence_type: str, consume: bool = False)`: Retrieves the next available number for a sequence (e.g., 'Income-Invoice') and optionally consumes it.
*   `register_company(company_data: CompanyRegister)`: Registers a new company under an accountant's account.

**4.6. Domain: Accountant (Feeds) - 6 Tools**
*Docs: No specific documentation file found for this domain.*

*   `register_feed(feed_name: str, feed_type: str)`: Creates a new data feed subscription for an accountant.
*   `list_feeds()`: Retrieves all registered feeds for the account.
*   `get_feed_items(feed_name: str)`: Retrieves the list of pending items in a specific feed.
*   `download_feed_item_content(feed_name: str, item_id: str)`: Downloads the actual file content of a feed item.
*   `confirm_feed_item(feed_name: str, item_id: str)`: Marks a feed item as processed to prevent duplicates.
*   `delete_feed(feed_name: str)`: Deletes a feed subscription.

**4.7. Domain: Document & File - 4 Tools**
*Docs: [Get Files](billit_docs_markdown/get-files.md), [Include own PDF and Attachments in Invoice to Deliver](billit_docs_markdown/include-own-pdf-and-attachments-in-invoice-to-deliver.md)*

*   `list_documents(odata_filter: str = None, skip: int = 0, top: int = 120)`: Retrieves a list of generic documents.
*   `upload_document(file_path: str, metadata: dict)`: Uploads a file as a new document record.
*   `get_document(document_id: int)`: Retrieves metadata for a specific document.
*   `download_file(file_id: str)`: Downloads the raw binary content of any file in Billit (from an Order, Document, etc.) given its `FileID`.

**4.8. Domain: GLAccount & Journal - 3 Tools**
*Docs: [Ventilation Codes](billit_docs_markdown/ventilation-codes.md)*

*   `create_gl_account(account_data: GLAccountCreate)`: Creates a single General Ledger account.
*   `import_gl_accounts(accounts_data: List[GLAccountCreate])`: Bulk-imports multiple GL accounts.
*   `import_journal_entries(entries_data: List[JournalEntry])`: Imports a batch of accounting journal entries.

**4.9. Domain: ToProcess (OCR) - 3 Tools**
*Docs: [API For Receiving Supplier Invoices](billit_docs_markdown/api-for-receiving-supplier-invoices.md)*

*   `submit_document_for_processing(file_path: str, metadata: dict)`: Uploads a document (e.g., a supplier invoice PDF) to Billit's OCR processing queue.
*   `update_processing_request(upload_id: str, data: dict)`: Updates the metadata of a document that is being processed.
*   `cancel_processing_request(upload_id: str)`: Cancels an in-progress document processing task.

**4.10. Domain: Peppol (E-invoicing) - 7 Tools**
*Docs: [Who is a Einvoice Receiver](billit_docs_markdown/who-is-a-einvoice-receiver.md), [Send via Email When delivery as Einvoice is not Possible](billit_docs_markdown/send-via-email-when-delivery-as-einvoice-is-not-possible.md)*

*   `check_peppol_participant(identifier: str)`: Checks if a company is registered on the Peppol network using their VAT, CBE, GLN, or other identifier.
*   `register_peppol_participant(data: dict)`: Initiates the Peppol registration process for the current company.
*   `unregister_peppol_participant()`: Removes the company's Peppol registration.
*   `send_peppol_invoice(order_id: int)`: Sends a previously created order via the Peppol network.
*   `list_peppol_inbox()`: Retrieves incoming e-invoices from the Peppol inbox.
*   `confirm_peppol_invoice(inbox_item_id: str)`: Confirms and accepts an incoming e-invoice.
*   `refuse_peppol_invoice(inbox_item_id: str)`: Rejects an incoming e-invoice.

**4.11. Domain: Misc (Utilities) - 3 Tools**
*Docs: [Types](billit_docs_markdown/types.md), [OData](billit_docs_markdown/odata.md)*

*   `search_company(keywords: str)`: Searches for a company by name or number in public registries.
*   `get_type_codes(code_type: str)`: Retrieves a list of predefined system codes (e.g., 'VATRate', 'Currency', 'OrderStatus').
*   `get_code_detail(code_type: str, code_key: str)`: Retrieves the details for a single system code.

**4.12. Domain: Reports - 2 Tools**

*   `list_available_reports()`: Retrieves a list of all report types that can be generated.
*   `get_report(report_id: str)`: Triggers the generation of a specific report and returns its content (e.g., as a file download).

**4.13. Domain: Webhook - 4 Tools**
*Docs: [Webhooks](billit_docs_markdown/webhooks.md), [Use webhooks to catch E-Invoice statuses](billit_docs_markdown/use-webhooks-to-catch-e-invoice-statuses.md)*

*   `create_webhook(url: str, entity_type: str, update_type: str)`: Creates a new webhook subscription.
*   `list_webhooks()`: Retrieves all configured webhooks for the account.
*   `delete_webhook(webhook_id: str)`: Deletes a webhook subscription.
*   `refresh_webhook_secret(webhook_id: str)`: Generates a new signing secret for a webhook.

**4.14. AI-Enhanced Composite Tools - 11 Tools**

*   `suggest_payment_reconciliation()`: Matches open invoices with bank transactions.
*   `generate_invoice_summary(start_date: str, end_date: str)`: Provides a summary of sales invoices.
*   `generate_expense_summary(start_date: str, end_date: str)`: Provides a summary of purchase invoices.
*   `get_cashflow_overview(period: str)`: Summarizes income vs. expenses.
*   `categorize_expense_invoice(invoice_id: int)`: Suggests expense categories for a purchase invoice.
*   `list_overdue_invoices()`: Returns a list of all unpaid invoices past their due date.
*   `get_supplier_spend_summary(supplier_id: int, period: str)`: Analyzes total spending with a specific supplier.
*   `get_customer_revenue_summary(customer_id: int, period: str)`: Analyzes total revenue from a specific customer.
*   `find_duplicate_contacts(similarity_threshold: float = 0.9)`: Scans for potential duplicate customers or suppliers.
*   `normalize_contact_address(party_id: int)`: Attempts to clean and standardize a contact's address.
*   `create_invoice_from_text(text_description: str)`: (Experimental) Parses natural language to create a draft invoice.

---

#### **5. Key Implementation Details**

**5.1. Pydantic Models & Field Aliasing**
We will use Pydantic's `Field(alias=...)` to map Billit's PascalCase JSON keys to Pythonic snake_case attributes for cleaner code.

```python
# In models/order.py
class Order(BaseModel):
    order_id: int = Field(..., alias="OrderID")
    order_type: str = Field(..., alias="OrderType")
    order_direction: str = Field(..., alias="OrderDirection")
    # ... etc.

    class Config:
        allow_population_by_field_name = True
```

**5.2. Error Handling**
The central `BillitAPIClient` will handle HTTP status codes and translate them into the standard response envelope.

*   **400 Bad Request:** The client will parse the `errors` array from the response body and include the `Code` and `Description` in the standardized error response.
*   **401 Unauthorized:** Logged as a critical configuration error.
*   **404 Not Found:** Handled gracefully, returning `success: false` with a "Not Found" message.
*   **429 Too Many Requests:** The client will automatically pause and retry based on the `Retry-After` header.
*   **5xx Server Error:** The client will perform a configurable number of retries with exponential backoff before returning a server error.

**5.3. Rate Limiting**
A token bucket algorithm will be implemented in the `BillitAPIClient` to proactively limit outgoing requests to the configured `RATE_LIMIT_PER_MINUTE`, preventing 429 errors.

---

#### **6. Testing Strategy**

*   **Unit Tests (`pytest`):** Every tool and utility function will have unit tests. The Billit API will be mocked using `respx` to simulate various success and error responses.
*   **Integration Tests (`pytest`):** A separate suite of tests will run against the **Billit Sandbox**. These tests will execute end-to-end workflows (e.g., create customer -> create invoice -> send -> record payment) to validate real-world behavior. These will be marked to run manually to avoid slowing down development.

---

#### **7. Deployment**

The application will be run using a production-ready web server like Uvicorn. The `uvicorn` command provided in the "Run the Server" section is suitable for development, and a similar command can be used for production, typically without the `--reload` flag.

```bash
# Example production run command
poetry run uvicorn server:app --host 0.0.0.0 --port 8000
```