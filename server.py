from fastapi import FastAPI

from billit.tools import (
    account,
    accountant,
    ai_composite,
    document,
    financial_transaction,
    gl_account,
    misc,
    order,
    party,
    peppol,
    product,
    reports,
    to_process,
    webhook,
)

app = FastAPI(title="Billit MCP")

app.include_router(party.router)
app.include_router(product.router)
app.include_router(order.router)
app.include_router(account.router)
app.include_router(financial_transaction.router)
app.include_router(accountant.router)
app.include_router(document.router)
app.include_router(gl_account.router)
app.include_router(to_process.router)
app.include_router(peppol.router)
app.include_router(misc.router)
app.include_router(reports.router)
app.include_router(webhook.router)
app.include_router(ai_composite.router)
