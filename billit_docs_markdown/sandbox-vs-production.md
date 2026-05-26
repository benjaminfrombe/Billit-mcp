---
title: "Sandbox VS Production"
updated: 2026-05-26
source_url: "https://docs.billit.be/docs/sandbox-vs-production-1"
source_slug: "sandbox-vs-production-1"
category: "getting-started-authentication"
topics:
  - getting
  - started
  - authentication
  - sandbox
  - vs
  - production
---

# Sandbox VS Production

Billit provides two distinct environments tailored for developers.

- **Production** \- connected to live accounting data and e-invoicing networks. Use this environment only for real business operations.
- **Sandbox** \- a safe replica of the production setup, designed for testing. Sandbox traffic reaches test government entities or test e-invoice networks, making it ideal for integration testing and experimentation.

By separating these environments, developers can test safely while ensuring compliance and data integrity in production.

### Environment URLs

| Isolated test environment | URL(s) | Type of Use | Notes |
| --- | --- | --- | --- |
| **Sandbox (Test)** | [https://my.sandbox.billit.be](https://my.sandbox.billit.be/) | User Interface | Use for all development and test cases. |
|  | [https://api.sandbox.billit.be](https://api.sandbox.billit.be/) | API | If you want to create account on sandbox : [Create new Sandbox account](https://my.sandbox.billit.be/Account/Register) |
| **Production (Live)** | [https://my.billit.be](https://my.billit.be/) | User Interface | Use only for real business operations. |
|  | [https://api.billit.be](https://api.billit.be/) | API | If you want to create account on production : [Create new production account here](https://my.billit.be/Account/Register) |

**⚠️ Important:**

- Always test your integration thoroughly in sandbox before switching to production.
- Calls to the production API trigger real invoices and transactions.

## Checklist

- [x]  Learn the **difference** between Sandbox & Production
- [x]  Create a new **Sandbox account** using a valid VAT number and email address

Updated5 months ago
