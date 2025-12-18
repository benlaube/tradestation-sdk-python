"""
Mock API response data for TradeStation SDK tests.

Provides realistic mock responses matching TradeStation API v3 structure.
All responses are dictionaries matching actual API response formats.
"""

# Account Responses

MOCK_ACCOUNTS_LIST = {
    "Accounts": [
        {
            "AccountID": "SIM123456",
            "AccountType": "INDIVIDUAL",
            "Status": "ACTIVE",
            "Currency": "USD",
            "Alias": "Paper Trading",
        },
        {
            "AccountID": "SIM789012",
            "AccountType": "INDIVIDUAL",
            "Status": "ACTIVE",
            "Currency": "USD",
            "Alias": "Paper 2",
        },
    ]
}

MOCK_ACCOUNT_BALANCES = {
    "Account": {
        "AccountID": "SIM123456",
        "AccountType": "INDIVIDUAL",
        "Status": "ACTIVE",
        "Currency": "USD",
        "Alias": "Paper Trading",
    },
    "Balances": {
        "Equity": "100000.00",
        "CashBalance": "100000.00",
        "BuyingPower": "400000.00",
        "DayTradingBuyingPower": "200000.00",
        "MarginAvailable": "300000.00",
        "MarginUsed": "0.00",
        "MaintenanceMargin": "0.00",
        "InitialMarginRequirement": "0.00",
        "NetLiquidationValue": "100000.00",
        "OpenPnL": "0.00",
        "RealizedPnL": "0.00",
        "UnrealizedPnL": "0.00",
    },
}

MOCK_DETAILED_BALANCES = {
    "Balances": [
        {"AccountID": "SIM123456", "Equity": "100000.00", "CashBalance": "100000.00", "BuyingPower": "400000.00"}
    ]
}

MOCK_BOD_BALANCES = {
    "Balances": [
        {
            "AccountID": "SIM123456",
            "Date": "2025-12-04",
            "Equity": "100000.00",
            "CashBalance": "100000.00",
            "BuyingPower": "400000.00",
            "MarginUsed": "0.00",
            "NetLiquidationValue": "100000.00",
        }
    ]
}

# Market Data Responses

MOCK_BARS_RESPONSE = {
    "Bars": [
        {
            "Time": "2025-12-04T09:30:00-05:00",
            "Open": 25000.0,
            "High": 25010.0,
            "Low": 24990.0,
            "Close": 25005.0,
            "Volume": 1000,
        },
        {
            "Time": "2025-12-04T09:31:00-05:00",
            "Open": 25005.0,
            "High": 25015.0,
            "Low": 25000.0,
            "Close": 25010.0,
            "Volume": 1200,
        },
    ]
}

MOCK_QUOTE_SNAPSHOT = {
    "Quotes": [
        {
            "Symbol": "MNQZ25",
            "Bid": 25000.0,
            "Ask": 25001.0,
            "Last": 25000.5,
            "Volume": 5000,
            "Open": 24990.0,
            "High": 25010.0,
            "Low": 24985.0,
            "Close": 25000.5,
        }
    ]
}

MOCK_SYMBOL_DETAILS = {
    "Symbols": [
        {
            "Symbol": "MNQZ25",
            "Description": "Micro E-mini Nasdaq-100 Futures",
            "AssetType": "FUTURE",
            "Exchange": "CME",
            "Currency": "USD",
        }
    ]
}

MOCK_SYMBOL_SEARCH = {
    "Symbols": [
        {"Symbol": "MNQZ25", "Description": "Micro E-mini Nasdaq-100 Futures", "AssetType": "FUTURE"},
        {"Symbol": "MNQH26", "Description": "Micro E-mini Nasdaq-100 Futures", "AssetType": "FUTURE"},
    ]
}

MOCK_FUTURES_INDEX_SYMBOLS = {"SymbolNames": ["MNQZ25", "MNQH26", "ESZ25", "ESH26"]}

MOCK_CRYPTO_SYMBOLS = {"SymbolNames": ["BTCUSD", "ETHUSD", "SOLUSD"]}

MOCK_OPTION_EXPIRATIONS = {"Expirations": ["2025-12-19", "2025-12-26", "2026-01-16"]}

MOCK_OPTION_STRIKES = {"Strikes": [25000, 25050, 25100, 25150, 25200]}

MOCK_OPTION_SPREAD_TYPES = {"SpreadTypes": ["VERTICAL", "CALENDAR", "BUTTERFLY", "IRON_CONDOR"]}

MOCK_OPTION_RISK_REWARD = {"RiskReward": {"MaxProfit": 1000.0, "MaxLoss": -500.0, "Breakeven": 25000.0}}

# Order Responses

MOCK_ORDER_PLACEMENT_SUCCESS = {
    "Orders": [
        {
            "OrderID": "924243071",
            "AccountID": "SIM123456",
            "Symbol": "MNQZ25",
            "TradeAction": "Buy",
            "OrderType": "Market",
            "Quantity": "2",
            "Status": "OPEN",
            "TimeInForce": {"Duration": "DAY"},
        }
    ]
}

MOCK_ORDER_CANCEL_SUCCESS = {"Orders": [{"OrderID": "924243071", "Status": "CANCELED"}]}

MOCK_ORDER_MODIFY_SUCCESS = {
    "Orders": [{"OrderID": "924243071", "Quantity": "3", "LimitPrice": "25010.00", "Status": "OPEN"}]
}

MOCK_CURRENT_ORDERS = {
    "Orders": [
        {
            "OrderID": "924243071",
            "AccountID": "SIM123456",
            "Symbol": "MNQZ25",
            "TradeAction": "Buy",
            "OrderType": "Limit",
            "Quantity": "2",
            "LimitPrice": "25000.00",
            "Status": "OPEN",
            "TimeInForce": {"Duration": "DAY"},
        }
    ],
    "NextToken": None,
}

MOCK_ORDER_HISTORY = {
    "Orders": [
        {
            "OrderID": "924243070",
            "AccountID": "SIM123456",
            "Symbol": "MNQZ25",
            "TradeAction": "Buy",
            "OrderType": "Market",
            "Quantity": "1",
            "Status": "FILLED",
            "FilledQuantity": "1",
            "AverageFillPrice": "25000.00",
            "TimeInForce": {"Duration": "DAY"},
        }
    ]
}

MOCK_ORDER_EXECUTIONS = {
    "Executions": [
        {
            "ExecutionID": "EX123456",
            "OrderID": "924243071",
            "Quantity": "2",
            "Price": "25000.00",
            "Time": "2025-12-04T10:00:00-05:00",
        }
    ]
}

MOCK_ORDER_CONFIRM = {"IsValid": True, "Warnings": [], "Errors": []}

MOCK_GROUP_ORDER_PLACEMENT = {
    "OrderGroups": [
        {
            "GroupID": "GRP123456",
            "GroupType": "BRK",
            "Orders": [{"OrderID": "924243071", "Status": "OPEN"}, {"OrderID": "924243072", "Status": "OPEN"}],
        }
    ]
}

MOCK_ACTIVATION_TRIGGERS = {
    "Triggers": [
        {"Key": "Last", "Description": "Last Price"},
        {"Key": "Bid", "Description": "Bid Price"},
        {"Key": "Ask", "Description": "Ask Price"},
    ]
}

MOCK_ROUTES = {
    "Routes": [
        {"Route": "TS", "Description": "TradeStation"},
        {"Route": "ISE", "Description": "International Securities Exchange"},
    ]
}

# Position Responses

MOCK_POSITIONS = {
    "Positions": [
        {
            "AccountID": "SIM123456",
            "Symbol": "MNQZ25",
            "Quantity": "2",
            "AveragePrice": "25000.00",
            "MarketValue": "50000.00",
            "UnrealizedPnL": "10.00",
        }
    ]
}

MOCK_EMPTY_POSITIONS = {"Positions": []}

# Streaming Responses (newline-delimited JSON)

MOCK_STREAM_QUOTE = '{"Type":"Quote","Symbol":"MNQZ25","Bid":25000.0,"Ask":25001.0,"Last":25000.5}\n'
MOCK_STREAM_ORDER = '{"Type":"Order","OrderID":"924243071","Status":"FILLED"}\n'
MOCK_STREAM_POSITION = '{"Type":"Position","Symbol":"MNQZ25","Quantity":"2"}\n'
MOCK_STREAM_BALANCE = '{"Type":"Balance","AccountID":"SIM123456","Equity":"100000.00"}\n'
MOCK_STREAM_STATUS_END = '{"Type":"StreamStatus","Status":"EndSnapshot"}\n'
MOCK_STREAM_STATUS_GOAWAY = '{"Type":"StreamStatus","Status":"GoAway"}\n'
MOCK_STREAM_ERROR = '{"Type":"Error","Error":"Connection lost"}\n'

# Error Responses

MOCK_ERROR_401 = {"Error": "Unauthorized", "Code": "AUTH_FAILED"}

MOCK_ERROR_400 = {"Error": "Invalid request", "Code": "INVALID_REQUEST"}

MOCK_ERROR_429 = {"Error": "Rate limit exceeded", "Code": "RATE_LIMIT"}

MOCK_ERROR_500 = {"Error": "Internal server error", "Code": "SERVER_ERROR"}

MOCK_ERROR_ARRAY = {"Errors": [{"Error": "Invalid symbol", "Code": "INVALID_SYMBOL"}]}

MOCK_OAUTH_ERROR = {"error": "invalid_grant", "error_description": "The provided authorization code is invalid"}

# Token Responses

MOCK_TOKEN_RESPONSE = {
    "access_token": "mock_access_token_12345",
    "refresh_token": "mock_refresh_token_67890",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "MarketData ReadAccount Trade",
}

MOCK_TOKEN_REFRESH_RESPONSE = {
    "access_token": "new_access_token_12345",
    "refresh_token": "new_refresh_token_67890",
    "token_type": "Bearer",
    "expires_in": 3600,
}
