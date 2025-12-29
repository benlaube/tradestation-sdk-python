#!/usr/bin/env python3
"""
Generate JSON Schema file for all TradeStation SDK models.

This script exports all Pydantic model schemas to a single JSON file
that can be used for documentation, validation, and integration purposes.

Usage:
    python generate_model_schemas.py

Output:
    docs/reference/sdk-models-schema.json
"""

import json
from pathlib import Path

from models import (
    # Order Models
    TradeStationOrderRequest,
    TradeStationOrderGroupRequest,
    TradeStationOrderResponse,
    TradeStationOrderGroupResponse,
    TradeStationOrderLeg,
    TradeStationConditionalOrder,
    TradeStationMarketActivationRule,
    TradeStationTimeActivationRule,
    TradeStationTrailingStop,
    # Order Execution Models
    TradeStationExecutionResponse,
    # Bar Models
    BarResponse,
    BarsResponse,
    # Symbol Models
    SymbolDetail,
    SymbolDetailsResponse,
    SymbolSearchResponse,
    # Option Models
    OptionExpirationsResponse,
    OptionStrikesResponse,
    OptionRiskRewardResponse,
    OptionSpreadType,
    OptionSpreadTypesResponse,
    # Order Wrappers / Confirm
    OrdersWrapper,
    CancelOrderResponse,
    ConfirmOrderResponse,
    ConfirmGroupOrderResponse,
    # Streaming Models
    QuoteStream,
    OrderStream,
    PositionStream,
    BalanceStream,
    BarStream,
    OptionChainStream,
    OptionQuoteStream,
    MarketDepthQuoteStream,
    MarketDepthAggregateStream,
    StreamStatus,
    Heartbeat,
    StreamErrorResponse,
    MarketFlags,
    # Account Models
    AccountSummary,
    BalanceDetail,
    AccountBalancesResponse,
    BODBalance,
    BODBalancesResponse,
    AccountsListResponse,
    # Position Models
    PositionResponse,
    PositionsResponse,
    # Quote Models
    QuoteSnapshot,
    QuotesResponse,
)


def generate_schema_file():
    """Generate JSON schema file for all SDK models."""
    
    # Organize models by category
    schemas = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "TradeStation SDK Models Schema",
        "description": "Complete JSON schema for all TradeStation SDK request, response, and streaming models",
        "version": "1.0.0",
        "_regeneration_instructions": {
            "note": "This file is auto-generated. Do not edit manually.",
            "how_to_regenerate": "Run the following command from the SDK root directory: python generate_model_schemas.py",
            "when_to_regenerate": "Regenerate this file whenever Pydantic models in the models/ directory are added, modified, or removed",
            "script_location": "generate_model_schemas.py",
            "output_location": "docs/reference/sdk-models-schema.json"
        },
        "models": {
            "orders": {
                "TradeStationOrderRequest": TradeStationOrderRequest.model_json_schema(),
                "TradeStationOrderGroupRequest": TradeStationOrderGroupRequest.model_json_schema(),
                "TradeStationOrderResponse": TradeStationOrderResponse.model_json_schema(),
                "TradeStationOrderGroupResponse": TradeStationOrderGroupResponse.model_json_schema(),
                "TradeStationOrderLeg": TradeStationOrderLeg.model_json_schema(),
                "TradeStationConditionalOrder": TradeStationConditionalOrder.model_json_schema(),
                "TradeStationMarketActivationRule": TradeStationMarketActivationRule.model_json_schema(),
                "TradeStationTimeActivationRule": TradeStationTimeActivationRule.model_json_schema(),
                "TradeStationTrailingStop": TradeStationTrailingStop.model_json_schema(),
            },
            "order_executions": {
                "TradeStationExecutionResponse": TradeStationExecutionResponse.model_json_schema(),
            },
            "order_wrappers": {
                "OrdersWrapper": OrdersWrapper.model_json_schema(),
                "CancelOrderResponse": CancelOrderResponse.model_json_schema(),
                "ConfirmOrderResponse": ConfirmOrderResponse.model_json_schema(),
                "ConfirmGroupOrderResponse": ConfirmGroupOrderResponse.model_json_schema(),
            },
            "bars": {
                "BarResponse": BarResponse.model_json_schema(),
                "BarsResponse": BarsResponse.model_json_schema(),
            },
            "symbols": {
                "SymbolDetail": SymbolDetail.model_json_schema(),
                "SymbolDetailsResponse": SymbolDetailsResponse.model_json_schema(),
                "SymbolSearchResponse": SymbolSearchResponse.model_json_schema(),
            },
            "options": {
                "OptionExpirationsResponse": OptionExpirationsResponse.model_json_schema(),
                "OptionStrikesResponse": OptionStrikesResponse.model_json_schema(),
                "OptionRiskRewardResponse": OptionRiskRewardResponse.model_json_schema(),
                "OptionSpreadType": OptionSpreadType.model_json_schema(),
                "OptionSpreadTypesResponse": OptionSpreadTypesResponse.model_json_schema(),
            },
            "streaming": {
                "QuoteStream": QuoteStream.model_json_schema(),
                "OrderStream": OrderStream.model_json_schema(),
                "PositionStream": PositionStream.model_json_schema(),
                "BalanceStream": BalanceStream.model_json_schema(),
                "BarStream": BarStream.model_json_schema(),
                "OptionChainStream": OptionChainStream.model_json_schema(),
                "OptionQuoteStream": OptionQuoteStream.model_json_schema(),
                "MarketDepthQuoteStream": MarketDepthQuoteStream.model_json_schema(),
                "MarketDepthAggregateStream": MarketDepthAggregateStream.model_json_schema(),
                "StreamStatus": StreamStatus.model_json_schema(),
                "Heartbeat": Heartbeat.model_json_schema(),
                "StreamErrorResponse": StreamErrorResponse.model_json_schema(),
                "MarketFlags": MarketFlags.model_json_schema(),
            },
            "accounts": {
                "AccountSummary": AccountSummary.model_json_schema(),
                "BalanceDetail": BalanceDetail.model_json_schema(),
                "AccountBalancesResponse": AccountBalancesResponse.model_json_schema(),
                "BODBalance": BODBalance.model_json_schema(),
                "BODBalancesResponse": BODBalancesResponse.model_json_schema(),
                "AccountsListResponse": AccountsListResponse.model_json_schema(),
            },
            "positions": {
                "PositionResponse": PositionResponse.model_json_schema(),
                "PositionsResponse": PositionsResponse.model_json_schema(),
            },
            "quotes": {
                "QuoteSnapshot": QuoteSnapshot.model_json_schema(),
                "QuotesResponse": QuotesResponse.model_json_schema(),
            },
        },
    }
    
    # Write to file
    output_path = Path(__file__).parent / "docs" / "reference" / "sdk-models-schema.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schemas, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated schema file: {output_path}")
    print(f"   Total models: {sum(len(category) for category in schemas['models'].values())}")
    print(f"   Categories: {len(schemas['models'])}")
    
    return output_path


if __name__ == "__main__":
    generate_schema_file()
