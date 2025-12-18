# TradeStation API v3 Structure Diagram

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-05-2025 14:02:18 EST
- **Version:** 1.0
- **Description:** Visual diagram showing TradeStation API v3 endpoint structure organized by tag groups (Brokerage, MarketData, Order Execution)
- **Type:** Architecture Diagram - Technical reference for developers and AI agents
- **Applicability:** When understanding API structure, planning SDK enhancements, or reviewing endpoint coverage
- **Dependencies:**
  - [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json) - Source OpenAPI specification
  - [`API_STRUCTURE_DETAILED.md`](./API_STRUCTURE_DETAILED.md) - Related detailed endpoint relationship diagram
- **How to Use:** Open this file in Cursor/VS Code markdown preview (Cmd+Shift+V / Ctrl+Shift+V), view on GitHub, or paste the Mermaid code into [Mermaid Live Editor](https://mermaid.live) to see the rendered diagram

---

## API Structure Overview

```mermaid
graph TB
    subgraph API["TradeStation API v3"]
        direction TB
        subgraph Brokerage["Brokerage"]
            v3brokerageaccounts["GET /v3/brokerage/accounts"]
            v3brokerageaccountsaccountsbal["GET /v3/brokerage/accounts/{accounts}/balances"]
            v3brokerageaccountsaccountsbod["GET /v3/brokerage/accounts/{accounts}/bodbalances"]
            v3brokerageaccountsaccountshis["GET /v3/brokerage/accounts/{accounts}/historicalorders"]
            v3brokerageaccountsaccountshis2["GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}"]
            v3brokerageaccountsaccountsord["GET /v3/brokerage/accounts/{accounts}/orders"]
            v3brokerageaccountsaccountsord2["GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}"]
            v3brokerageaccountsaccountspos["GET /v3/brokerage/accounts/{accounts}/positions"]
            v3brokeragestreamaccountsaccou["GET /v3/brokerage/stream/accounts/{accounts}/orders"]
            v3brokeragestreamaccountsaccou2["GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}"]
            v3brokeragestreamaccountsaccou3["GET /v3/brokerage/stream/accounts/{accounts}/positions"]
        end
        subgraph MarketData["MarketData"]
            v3marketdatabarchartssymbol["GET /v3/marketdata/barcharts/{symbol}"]
            v3marketdatastreambarchartssym["GET /v3/marketdata/stream/barcharts/{symbol}"]
            v3marketdatasymbollistscryptop["GET /v3/marketdata/symbollists/cryptopairs/symbolnames"]
            v3marketdatasymbolssymbols["GET /v3/marketdata/symbols/{symbols}"]
            v3marketdataoptionsexpirations["GET /v3/marketdata/options/expirations/{underlying}"]
            v3marketdataoptionsriskreward["POST /v3/marketdata/options/riskreward"]
            v3marketdataoptionsspreadtypes["GET /v3/marketdata/options/spreadtypes"]
            v3marketdataoptionsstrikesunde["GET /v3/marketdata/options/strikes/{underlying}"]
            v3marketdatastreamoptionschain["GET /v3/marketdata/stream/options/chains/{underlying}"]
            v3marketdatastreamoptionsquote["GET /v3/marketdata/stream/options/quotes"]
            v3marketdataquotessymbols["GET /v3/marketdata/quotes/{symbols}"]
            v3marketdatastreamquotessymbol["GET /v3/marketdata/stream/quotes/{symbols}"]
            v3marketdatastreammarketdepthq["GET /v3/marketdata/stream/marketdepth/quotes/{symbol}"]
            v3marketdatastreammarketdeptha["GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}"]
        end
        subgraph OrderExecution["Order Execution"]
            v3orderexecutionorderconfirm["POST /v3/orderexecution/orderconfirm"]
            v3orderexecutionordergroupconf["POST /v3/orderexecution/ordergroupconfirm"]
            v3orderexecutionordergroups["POST /v3/orderexecution/ordergroups"]
            v3orderexecutionorders["POST /v3/orderexecution/orders"]
            v3orderexecutionordersorderID["PUT /v3/orderexecution/orders/{orderID}"]
            v3orderexecutionordersorderID2["DELETE /v3/orderexecution/orders/{orderID}"]
            v3orderexecutionactivationtrig["GET /v3/orderexecution/activationtriggers"]
            v3orderexecutionroutes["GET /v3/orderexecution/routes"]
        end
    end
```

---

## Endpoint Summary

- **Brokerage:** 11 endpoints (account, position, order management)
- **MarketData:** 14 endpoints (market data, quotes, symbols, streaming)
- **Order Execution:** 8 endpoints (order placement, modification, cancellation)
- **Total:** 33 v3 endpoints

---

## How to View This Diagram

### In Cursor/VS Code
- The diagram will render automatically in the markdown preview
- Open this file and use the preview pane (Cmd+Shift+V / Ctrl+Shift+V)

### In GitHub
- Navigate to the file on GitHub - diagrams render automatically

### Online
- Copy the Mermaid code block and paste into [Mermaid Live Editor](https://mermaid.live)
- Or use any Mermaid-compatible viewer

### In Other Markdown Viewers
- Most modern markdown viewers (Obsidian, Typora, etc.) support Mermaid diagrams
- Some may require Mermaid plugin/extension

---

**Related Files:**
- [`API_STRUCTURE_DETAILED.md`](./API_STRUCTURE_DETAILED.md) - Detailed endpoint relationships
- [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json) - Complete OpenAPI specification
