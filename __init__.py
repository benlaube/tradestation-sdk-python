"""
TradeStation SDK - Internal Implementation

Self-contained SDK for TradeStation API v3 operations.
Replaces external tastyware/tradestation SDK dependency.

Dependencies: All tradestation SDK submodules
"""

from typing import Any

# Import operation modules
from .operations.accounts import AccountOperations
from .utils.client import HTTPClient, get_base_url
from .config import sdk_config
from .exceptions import (
    AuthenticationError,
    InvalidRequestError,
    InvalidTokenError,
    NetworkError,
    RateLimitError,
    TokenExpiredError,
    TradeStationAPIError,
)
from .utils.logger import setup_logger

# Import mappers
from .utils.mappers import (
    normalize_account,
    normalize_account_balances,
    normalize_bod_balance,
    normalize_balances,
    normalize_execution,
    normalize_order,
    normalize_position,
    normalize_quote,
)
from .operations.market_data import MarketDataOperations
from .models.accounts import (
    AccountBalancesResponse,
    AccountSummary,
    BalanceDetail,
    BODBalance,
    BODBalancesResponse,
)
from .models.accounts_list import AccountsListResponse
from .models.order_executions import (
    TradeStationExecutionResponse,
)

# Import models
from .models.orders import (
    TradeStationConditionalOrder,
    TradeStationMarketActivationRule,
    TradeStationOrderGroupRequest,
    TradeStationOrderGroupResponse,
    TradeStationOrderLeg,
    TradeStationOrderRequest,
    TradeStationOrderResponse,
    TradeStationTimeActivationRule,
    TradeStationTrailingStop,
)
from .models.positions import PositionResponse, PositionsResponse
from .models.quotes import QuoteSnapshot, QuotesResponse
from .models.streaming import (
    BalanceStream,
    BarStream,
    Heartbeat,
    MarketFlags,
    OrderStream,
    PositionStream,
    QuoteStream,
    StreamErrorResponse,
    StreamStatus,
)
from .operations.order_executions import OrderExecutionOperations
from .operations.orders import OrderOperations
from .operations.positions import PositionOperations

# Import core SDK components
from .session import OAuthCallbackHandler, Session, TokenManager
from .operations.streaming import StreamingManager, WebSocketManager

logger = setup_logger(__name__, sdk_config.log_level)

__version__ = "1.0.1"


class TradeStationSDK:
    """
    High-level façade for the internal TradeStation SDK.

    This class wires together authentication, HTTP client, domain-specific
    operation modules (accounts, market data, orders, positions, executions),
    and streaming helpers. All public methods delegate to the underlying
    operation classes while keeping a consistent interface and shared state
    (active account ID, last authenticated mode, logging).

    Key behaviors:
    - Centralizes OAuth2/token lifecycle and HTTP client configuration
    - Provides PAPER/LIVE mode awareness across all operations
    - Normalizes return shapes (dicts/lists) from Pydantic models for callers
    - Exposes streaming managers for HTTP streaming and optional SDK websockets
    """

    def __init__(self, enable_full_logging: bool = False, use_async: bool = False):
        """
        Bootstrap the SDK with shared dependencies and operation modules.

        Args:
            enable_full_logging: If True, include full HTTP request/response bodies in logs.
                Use sparingly—may expose sensitive data. Can also be set via
                `TRADESTATION_FULL_LOGGING` env var.
            use_async: If True, enable async HTTP client (httpx) for non-blocking I/O.
                Default False for backward compatibility. Can also be set via
                `TRADESTATION_USE_ASYNC` env var.

        Side Effects:
            - Instantiates TokenManager and HTTPClient
            - Binds Account/MarketData/Orders/Positions/Executions modules
            - Sets default trading mode from `sdk_config.trading_mode`
        """
        self.client_id = sdk_config.client_id
        self.client_secret = sdk_config.client_secret
        self.redirect_uri = sdk_config.redirect_uri
        self.account_id = sdk_config.account_id
        # Store default mode - initialized from secrets, but can be updated from last authenticated mode
        # Users authenticate one mode at a time, so we can use the last authenticated mode as default
        self.default_mode = sdk_config.trading_mode

        # Base URLs for both modes
        self.paper_base_url = "https://sim-api.tradestation.com/v3"
        self.live_base_url = "https://api.tradestation.com/v3"

        # Initialize TokenManager
        self._token_manager = TokenManager(
            client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri
        )

        # Check environment variable for async mode
        env_async = sdk_config.use_async
        effective_async = use_async or env_async

        # Initialize HTTPClient with full logging and async options
        self._client = HTTPClient(
            self._token_manager, enable_full_logging=enable_full_logging, use_async=effective_async
        )

        # Initialize operation modules with default account_id and mode
        self._accounts = AccountOperations(self._client, self.account_id, self.default_mode)
        self._market_data = MarketDataOperations(self._client)
        self._positions = PositionOperations(self._client, self._accounts, self.account_id, self.default_mode)
        self._order_executions = OrderExecutionOperations(
            self._client, self._accounts, self.account_id, self.default_mode
        )
        self._orders = OrderOperations(self._client, self._accounts, self.account_id, self.default_mode)
        # Pass HTTP client to StreamingManager for HTTP streaming support
        self._streaming = StreamingManager(self._token_manager, self.client_id, self.client_secret, self._client)

        logger.info("TradeStation SDK initialized with dual-mode support (PAPER and LIVE)")

    # Authentication methods - delegate to TokenManager
    def authenticate(self, mode: str | None = None):
        """
        Perform OAuth2 Authorization Code flow for PAPER or LIVE mode.

        Args:
            mode: Explicit trading mode ("PAPER" or "LIVE"). Defaults to current
                `self.default_mode` if omitted.

        Returns:
            Token payload dictionary produced by `TokenManager.authenticate`.

        Raises:
            AuthenticationError: If OAuth flow fails or user denies consent.
        """
        return self._token_manager.authenticate(mode)

    def refresh_access_token(self, mode: str | None = None):
        """
        Refresh an existing access token using the stored refresh token.

        Args:
            mode: Trading mode to refresh (PAPER/LIVE). Defaults to last mode.

        Returns:
            Updated token payload dictionary.

        Raises:
            TokenExpiredError | AuthenticationError: When refresh fails.
        """
        return self._token_manager.refresh_access_token(mode)

    def ensure_authenticated(self, mode: str | None = None):
        """
        Verify valid tokens exist and refresh if needed.

        Args:
            mode: Trading mode to validate (PAPER/LIVE). Defaults to last mode.

        Returns:
            True when a valid token is available.

        Raises:
            AuthenticationError: If refresh or auth fails.
        """
        return self._token_manager.ensure_authenticated(mode)

    @property
    def active_mode(self) -> str:
        """
        Resolve the currently active trading mode.

        Returns:
            Mode string ("PAPER" or "LIVE"). Prefers `TokenManager.last_mode`;
            falls back to `self.default_mode`. Also syncs `default_mode` to
            ensure subsequent calls stay consistent.
        """
        active = self._token_manager.last_mode
        # Update default mode to match active mode (users authenticate one mode at a time)
        if active:
            self.default_mode = active
        return active or self.default_mode

    # Account methods - delegate to AccountOperations
    def get_account_info(self, mode: str | None = None) -> dict:
        """
        Retrieve account metadata and select a working account ID.

        Args:
            mode: Trading mode (PAPER/LIVE). Defaults to active mode.

        Returns:
            Dict with keys: account_id, name, type, status, currency, accounts (full list).

        Side Effects:
            Updates `self.account_id` with the selected account.
        """
        result = self._accounts.get_account_info(mode)
        # Update account_id if found
        if result and result.get("account_id"):
            self.account_id = result.get("account_id")
        return result

    def get_account_balances(self, mode: str | None = None, account_id: str | None = None) -> dict[str, Any]:
        """
        Get summarized balances for a single account.

        Args:
            mode: Trading mode to query.
            account_id: Optional explicit account ID; otherwise uses detected default.

        Returns:
            Dict containing equity, cash, buying power, margin fields, and P&L metrics.
        """
        return self._accounts.get_account_balances(mode, account_id)

    def get_account_balances_detailed(self, account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]:
        """
        Get detailed balances for one or many accounts.

        Args:
            account_ids: Comma-separated IDs; if None, uses default account.
            mode: Trading mode to query.

        Returns:
            Dict with `Accounts` and `Errors` lists from the API response.
        """
        return self._accounts.get_account_balances_detailed(account_ids, mode)

    def get_account_balances_bod(self, account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]:
        """
        Get beginning-of-day balances for one or many accounts.

        Args:
            account_ids: Comma-separated IDs; if None, uses default account.
            mode: Trading mode to query.

        Returns:
            Dict with BOD balances and any API errors.
        """
        return self._accounts.get_account_balances_bod(account_ids, mode)

    # Market data methods - delegate to MarketDataOperations
    def get_bars(
        self, symbol: str, interval: str, unit: str, bars_back: int = 200, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Fetch historical OHLCV bars.

        Args:
            symbol: Trading symbol (e.g., "MESZ5", "AAPL").
            interval: Bar interval (e.g., "1", "5").
            unit: Interval unit ("Minute", "Daily", etc.).
            bars_back: Number of bars to pull when date range not provided.
            mode: Trading mode.

        Returns:
            List of bar dicts from TradeStation API.
        """
        return self._market_data.get_bars(symbol, interval, unit, bars_back, None, None, mode)

    def search_symbols(
        self, pattern: str = "", category: str = "Future", asset_type: str | None = None, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Search TradeStation symbol catalog.

        Args:
            pattern: Partial symbol to match.
            category: Asset class filter (Future, Stock, Option, Crypto).
            asset_type: Optional asset type filter.
            mode: Trading mode.

        Returns:
            List of symbol metadata dicts.
        """
        return self._market_data.search_symbols(pattern, category, asset_type, mode)

    def get_futures_index_symbols(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Retrieve common equity index futures symbols (mini/micro contracts).

        Args:
            mode: Trading mode.

        Returns:
            List of symbol metadata dicts for common index futures.
        """
        return self._market_data.get_futures_index_symbols(mode)

    def get_quote_snapshots(self, symbols: str, mode: str | None = None) -> dict[str, Any]:
        """
        Get full quote snapshots for one or many symbols.

        Args:
            symbols: Comma-separated list (max 100).
            mode: Trading mode.

        Returns:
            Dict containing `Quotes` list and `Errors` list.
        """
        return self._market_data.get_quote_snapshots(symbols, mode)

    def get_symbol_details(self, symbols: str, mode: str | None = None) -> dict[str, Any]:
        """
        Get symbol formatting and contract metadata.

        Args:
            symbols: Comma-separated list (max 50).
            mode: Trading mode.

        Returns:
            Dict containing `Symbols` list and `Errors` list.
        """
        return self._market_data.get_symbol_details(symbols, mode)

    # Position methods - delegate to PositionOperations
    def get_position(self, symbol: str, mode: str | None = None) -> int:
        """
        Get the net position quantity for a single symbol.

        Args:
            symbol: Trading symbol to inspect.
            mode: Trading mode. Defaults to active mode.

        Returns:
            Integer net position size (positive=long, negative=short, 0=flat).
        """
        return self._positions.get_position(symbol, mode)

    def get_all_positions(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        List all open positions on the active account.

        Args:
            mode: Trading mode. Defaults to active mode.

        Returns:
            List of position dictionaries including size, average price, and P&L.
        """
        return self._positions.get_all_positions(mode)

    def flatten_position(self, symbol: str | None = None, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Close one symbol or all positions via market orders.

        Args:
            symbol: If provided, only that symbol is flattened; otherwise all positions are closed.
            mode: Trading mode.

        Returns:
            List of order responses created to flatten the requested positions.
        """
        return self._positions.flatten_position(symbol, self._orders, mode)

    def get_todays_profit_loss(self, mode: str | None = None) -> float:
        """
        Compute today's P&L across all positions.

        Args:
            mode: Trading mode.

        Returns:
            Float P&L value for the current trading day.
        """
        return self._positions.get_todays_profit_loss(mode)

    def get_todays_trades(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get trades filled today.

        Args:
            mode: Trading mode.

        Returns:
            List of filled order dicts (status FLL/FLP) from the current day.
        """
        return self._positions.get_todays_trades(self._orders, mode)

    def get_unrealized_profit_loss(self, mode: str | None = None) -> float:
        """
        Calculate unrealized (open) P&L for all positions.

        Args:
            mode: Trading mode.

        Returns:
            Float unrealized P&L value.
        """
        return self._positions.get_unrealized_profit_loss(mode)

    def cancel_all_orders_for_symbol(
        self, symbol: str, account_ids: str | None = None, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Cancel every open order for a given symbol.

        Args:
            symbol: Symbol whose open orders should be canceled.
            account_ids: Optional comma-separated account IDs; defaults to active account.
            mode: Trading mode.

        Returns:
            List of cancel results per order ID.
        """
        return self._order_executions.cancel_all_orders_for_symbol(symbol, account_ids, mode)

    def cancel_all_orders(self, account_ids: str | None = None, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Cancel every open order for the specified accounts.

        Args:
            account_ids: Optional comma-separated IDs; defaults to active account.
            mode: Trading mode.

        Returns:
            List of cancel results per order ID.
        """
        return self._order_executions.cancel_all_orders(account_ids, mode)

    def replace_order(
        self,
        old_order_id: str,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "Market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "DAY",
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Cancel an existing order and submit a replacement in one call.

        Args:
            old_order_id: Order ID to replace.
            symbol: Symbol for the replacement order.
            side: "BUY" or "SELL".
            quantity: Order quantity.
            order_type: Market | Limit | Stop | StopLimit | TrailingStop.
            limit_price: Limit price if order_type requires it.
            stop_price: Stop price if order_type requires it.
            time_in_force: TIF code (e.g., DAY, GTC).
            trail_amount: Price trail amount (for trailing stops).
            trail_percent: Percentage trail (for trailing stops).
            mode: Trading mode.

        Returns:
            Tuple of (new_order_id, status_message).
        """
        return self._order_executions.replace_order(
            old_order_id,
            symbol,
            side,
            quantity,
            order_type,
            limit_price,
            stop_price,
            time_in_force,
            trail_amount,
            trail_percent,
            mode,
        )

    # Order execution methods - delegate to OrderExecutionOperations
    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "Market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "DAY",
        wait_for_fill: bool = False,
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        mode: str | None = None,
    ) -> tuple:
        """
        Place a single-leg order with optional wait-for-fill workflow.

        Args:
            symbol: Symbol to trade.
            side: BUY or SELL.
            quantity: Order quantity.
            order_type: Market | Limit | Stop | StopLimit | TrailingStop.
            limit_price: Optional limit price.
            stop_price: Optional stop/trigger price.
            time_in_force: TIF code (DAY/GTC, etc.).
            wait_for_fill: If True, polls until order is filled or terminal.
            trail_amount: Trailing amount in price units.
            trail_percent: Trailing percentage.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.place_order(
            symbol,
            side,
            quantity,
            order_type,
            limit_price,
            stop_price,
            time_in_force,
            wait_for_fill,
            trail_amount,
            trail_percent,
            mode,
        )

    def cancel_order(self, order_id: str, mode: str | None = None) -> tuple:
        """
        Cancel a single working order.

        Args:
            order_id: TradeStation order ID to cancel.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.cancel_order(order_id, mode)

    def modify_order(
        self,
        order_id: str,
        quantity: int | None = None,
        limit_price: float | None = None,
        stop_price: float | None = None,
        mode: str | None = None,
    ) -> tuple:
        """
        Modify a working order's quantity or prices.

        Args:
            order_id: Order ID to modify.
            quantity: Optional new quantity.
            limit_price: Optional new limit price.
            stop_price: Optional new stop/trigger price.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.modify_order(order_id, quantity, limit_price, stop_price, mode)

    def get_order_history(
        self, start_date: str | None = None, end_date: str | None = None, limit: int = 100, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Fetch historical orders within a time window.

        Args:
            start_date: ISO timestamp; defaults to 7 days back if None.
            end_date: ISO timestamp; defaults to now if None.
            limit: Max records (API default 1000).
            mode: Trading mode.

        Returns:
            List of order dictionaries.
        """
        return self._orders.get_order_history(start_date, end_date, limit, mode)

    def get_current_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Get active (non-terminal) orders with pagination support.

        Args:
            account_ids: Optional comma-separated IDs; defaults to active account.
            next_token: Pagination token from previous response.
            mode: Trading mode.

        Returns:
            Dict with `Orders`, optional `NextPageToken`, and `Errors`.
        """
        return self._orders.get_current_orders(account_ids, next_token, mode)

    def get_orders_by_status(
        self,
        status: str | list[str],
        account_ids: str | None = None,
        next_token: str | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve orders filtered by one or multiple statuses.

        Args:
            status: Single status code or list of codes (e.g., \"OPN\", \"FLL\").
            account_ids: Optional comma-separated account IDs.
            next_token: Pagination token.
            mode: Trading mode.

        Returns:
            Dict with `Orders`, optional `NextPageToken`, and `Errors`.
        """
        return self._orders.get_orders_by_status(status, account_ids, next_token, mode)

    def get_open_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Convenience wrapper to fetch only open/working orders.

        Args:
            account_ids: Optional comma-separated IDs.
            next_token: Pagination token.
            mode: Trading mode.

        Returns:
            Dict with `Orders`, optional `NextPageToken`, and `Errors`.
        """
        return self._orders.get_open_orders(account_ids, next_token, mode)

    def get_filled_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Convenience wrapper to fetch filled orders.

        Args:
            account_ids: Optional comma-separated IDs.
            next_token: Pagination token.
            mode: Trading mode.

        Returns:
            Dict with `Orders`, optional `NextPageToken`, and `Errors`.
        """
        return self._orders.get_filled_orders(account_ids, next_token, mode)

    def get_canceled_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Convenience wrapper to fetch canceled orders.

        Args:
            account_ids: Optional comma-separated IDs.
            next_token: Pagination token.
            mode: Trading mode.

        Returns:
            Dict with `Orders`, optional `NextPageToken`, and `Errors`.
        """
        return self._orders.get_canceled_orders(account_ids, next_token, mode)

    def get_rejected_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Convenience wrapper to fetch rejected orders.

        Args:
            account_ids: Optional comma-separated IDs.
            next_token: Pagination token.
            mode: Trading mode.

        Returns:
            Dict with `Orders`, optional `NextPageToken`, and `Errors`.
        """
        return self._orders.get_rejected_orders(account_ids, next_token, mode)

    def get_orders_by_ids(
        self, order_ids: str, account_ids: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Retrieve current orders by explicit order IDs.

        Args:
            order_ids: Comma-separated list of order IDs.
            account_ids: Optional comma-separated account IDs.
            mode: Trading mode.

        Returns:
            Dict with `Orders` list and `Errors`.
        """
        return self._orders.get_orders_by_ids(order_ids, account_ids, mode)

    def get_historical_orders_by_ids(
        self,
        order_ids: str,
        account_ids: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve historical orders by IDs within an optional date window.

        Args:
            order_ids: Comma-separated order IDs.
            account_ids: Optional account IDs.
            start_date: Optional start date ISO string.
            end_date: Optional end date ISO string.
            mode: Trading mode.

        Returns:
            Dict with `Orders` list and `Errors`.
        """
        return self._orders.get_historical_orders_by_ids(order_ids, account_ids, start_date, end_date, mode)

    def get_order_executions(self, order_id: str, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Fetch execution fills for a specific order.

        Args:
            order_id: Order ID to inspect.
            mode: Trading mode.

        Returns:
            List of execution dictionaries.
        """
        return self._order_executions.get_order_executions(order_id, mode)

    def is_order_filled(self, order_id: str, mode: str | None = None) -> bool:
        """
        Check whether a specific order is in a filled terminal state.

        Args:
            order_id: Order ID to check.
            mode: Trading mode.

        Returns:
            True if filled, False otherwise.
        """
        return self._order_executions.is_order_filled(order_id, mode)

    def confirm_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "Market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Validate an order without submitting it (pre-flight confirm).

        Args:
            symbol: Symbol to trade.
            side: BUY or SELL.
            quantity: Order quantity.
            order_type: Market | Limit | Stop | StopLimit.
            limit_price: Optional limit price.
            stop_price: Optional stop/trigger price.
            time_in_force: TIF code.
            mode: Trading mode.

        Returns:
            Dict with validation results and any warnings/errors.
        """
        return self._order_executions.confirm_order(
            symbol, side, quantity, order_type, limit_price, stop_price, time_in_force, mode
        )

    def get_activation_triggers(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        List available activation trigger keys for conditional orders.

        Args:
            mode: Trading mode.

        Returns:
            List of trigger metadata dicts.
        """
        return self._order_executions.get_activation_triggers(mode)

    def confirm_group_order(
        self, group_type: str, orders: list[dict[str, Any]], mode: str | None = None
    ) -> dict[str, Any]:
        """
        Validate an OCO/Bracket group without submitting.

        Args:
            group_type: "OCO" or "BRK".
            orders: List of order legs in TradeStation format.
            mode: Trading mode.

        Returns:
            Dict with validation results.
        """
        return self._order_executions.confirm_group_order(group_type, orders, mode)

    def place_group_order(
        self, group_type: str, orders: list[dict[str, Any]], mode: str | None = None
    ) -> dict[str, Any]:
        """
        Submit an OCO/Bracket group order.

        Args:
            group_type: "OCO" or "BRK".
            orders: List of order legs in TradeStation format.
            mode: Trading mode.

        Returns:
            Dict with group order response.
        """
        return self._order_executions.place_group_order(group_type, orders, mode)

    def get_routes(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        List available routing destinations for orders.

        Args:
            mode: Trading mode.

        Returns:
            List of routing option dicts.
        """
        return self._order_executions.get_routes(mode)

    # Convenience functions - delegate to OrderExecutionOperations
    def place_bracket_order(
        self,
        symbol: str,
        entry_side: str,
        quantity: int,
        profit_target: float,
        stop_loss: float | None = None,
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        use_trailing_stop: bool = False,
        entry_price: float | None = None,
        entry_order_type: str = "Market",
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Submit a bracket order (entry + OCO exits).

        Args:
            symbol: Underlying symbol.
            entry_side: BUY or SELL for entry leg.
            quantity: Order size.
            profit_target: Target price for take-profit leg.
            stop_loss: Optional stop-loss price.
            trail_amount: Optional trailing stop amount.
            trail_percent: Optional trailing stop percent.
            use_trailing_stop: If True, uses trailing stop instead of fixed stop.
            entry_price: Optional limit for entry if not market.
            entry_order_type: "Market" or "Limit".
            time_in_force: TIF code.
            mode: Trading mode.

        Returns:
            Dict with group order response.
        """
        return self._order_executions.place_bracket_order(
            symbol,
            entry_side,
            quantity,
            profit_target,
            stop_loss,
            trail_amount,
            trail_percent,
            use_trailing_stop,
            entry_price,
            entry_order_type,
            time_in_force,
            mode,
        )

    def place_oco_order(self, orders: list[dict[str, Any]], mode: str | None = None) -> dict[str, Any]:
        """
        Submit an OCO (One-Cancels-Other) order pair.

        Args:
            orders: Two-leg order list in TradeStation format.
            mode: Trading mode.

        Returns:
            Dict with group order response.
        """
        return self._order_executions.place_oco_order(orders, mode)

    def place_trailing_stop_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a single-leg trailing stop order.

        Args:
            symbol: Symbol to trade.
            side: BUY or SELL.
            quantity: Order quantity.
            trail_amount: Price trail amount.
            trail_percent: Percentage trail.
            time_in_force: TIF code.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.place_trailing_stop_order(
            symbol, side, quantity, trail_amount, trail_percent, time_in_force, mode
        )

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        limit_price: float,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a simple limit order.

        Args:
            symbol: Symbol to trade.
            side: BUY or SELL.
            quantity: Order quantity.
            limit_price: Limit price.
            time_in_force: TIF code.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.place_limit_order(symbol, side, quantity, limit_price, time_in_force, mode)

    def place_stop_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        stop_price: float,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a simple stop order.

        Args:
            symbol: Symbol to trade.
            side: BUY or SELL.
            quantity: Order quantity.
            stop_price: Stop trigger price.
            time_in_force: TIF code.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.place_stop_order(symbol, side, quantity, stop_price, time_in_force, mode)

    def place_stop_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        limit_price: float,
        stop_price: float,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a stop-limit order.

        Args:
            symbol: Symbol to trade.
            side: BUY or SELL.
            quantity: Order quantity.
            limit_price: Limit price once triggered.
            stop_price: Stop trigger price.
            time_in_force: TIF code.
            mode: Trading mode.

        Returns:
            Tuple of (order_id, status_message).
        """
        return self._order_executions.place_stop_limit_order(
            symbol, side, quantity, limit_price, stop_price, time_in_force, mode
        )

    # Streaming property
    @property
    def streaming(self) -> StreamingManager:
        """Get StreamingManager instance for HTTP streaming."""
        return self._streaming

    @property
    def session(self) -> StreamingManager | None:
        """Get streaming session. For backward compatibility."""
        return self._streaming.session

    def info(self) -> dict[str, Any]:
        """
        Get SDK information and diagnostics.

        Provides version, configuration, authentication status, and feature flags.
        Useful for debugging and verifying SDK setup.

        Returns:
            Dictionary with SDK version, configuration, and status including:
            - version: SDK version string
            - api_version: TradeStation API version
            - base_urls: API base URLs for PAPER and LIVE modes
            - authenticated_modes: List of modes with valid tokens
            - active_mode: Currently active trading mode
            - account_id: Current account ID (if available)
            - features: Dictionary of enabled features

        Example:
            >>> sdk = TradeStationSDK()
            >>> info = sdk.info()
            >>> print(f"SDK Version: {info['version']}")
            SDK Version: 1.0.0
            >>> print(f"Authenticated: {info['authenticated_modes']}")
            Authenticated: ['PAPER']
            >>> print(f"Features: {list(info['features'].keys())}")
            Features: ['streaming', 'convenience_functions', 'type_safety', 'full_logging']

        Dependencies: None
        """
        return {
            "version": __version__,
            "api_version": "v3",
            "base_urls": {
                "paper": self.paper_base_url,
                "live": self.live_base_url,
            },
            "authenticated_modes": [
                mode for mode in ["PAPER", "LIVE"] if self._token_manager.get_tokens(mode) is not None
            ],
            "active_mode": self.active_mode,
            "account_id": self.account_id,
            "features": {
                "streaming": True,
                "http_streaming": True,
                "convenience_functions": True,
                "type_safety": True,
                "automatic_reconnection": True,
                "rest_fallback": True,
                "full_logging": self._client.enable_full_logging,
                "error_categorization": True,
                "async_support": self._client.use_async,
            },
            "sdk_status": "production_ready",
            "python_version_required": ">=3.10",
        }

    # Internal accessors (for advanced use cases)
    @property
    def client(self) -> HTTPClient:
        """Get HTTP client instance."""
        return self._client

    @property
    def token_manager(self) -> TokenManager:
        """Get token manager instance."""
        return self._token_manager

    @property
    def accounts(self) -> AccountOperations:
        """Get account operations instance."""
        return self._accounts

    @property
    def market_data(self) -> MarketDataOperations:
        """Get market data operations instance."""
        return self._market_data

    @property
    def orders(self) -> OrderOperations:
        """Get order operations instance."""
        return self._orders

    @property
    def positions(self) -> PositionOperations:
        """Get position operations instance."""
        return self._positions

    @property
    def order_executions(self) -> OrderExecutionOperations:
        """Get order execution operations instance."""
        return self._order_executions

    async def aclose(self):
        """
        Close async HTTP client and release resources.

        Call this when done with async operations to properly clean up connections.
        Only needed if use_async=True was set during initialization.
        """
        if self._client.use_async:
            await self._client.aclose()


# Export main SDK class and all components
__all__ = [
    # Main SDK class
    "TradeStationSDK",
    # Core components
    "Session",
    "TokenManager",
    "OAuthCallbackHandler",
    "HTTPClient",
    "get_base_url",
    # Exceptions
    "TradeStationAPIError",
    "AuthenticationError",
    "RateLimitError",
    "InvalidRequestError",
    "NetworkError",
    "TokenExpiredError",
    "InvalidTokenError",
    # Operation modules
    "AccountOperations",
    "MarketDataOperations",
    "OrderExecutionOperations",
    "OrderOperations",
    "PositionOperations",
    "StreamingManager",
    "WebSocketManager",
    # Models (REST API)
    "TradeStationOrderRequest",
    "TradeStationOrderGroupRequest",
    "TradeStationOrderResponse",
    "TradeStationOrderGroupResponse",
    "TradeStationExecutionResponse",
    "TradeStationOrderLeg",
    "TradeStationConditionalOrder",
    "TradeStationMarketActivationRule",
    "TradeStationTimeActivationRule",
    "TradeStationTrailingStop",
    # Models (Streaming API)
    "QuoteStream",
    "OrderStream",
    "PositionStream",
    "BalanceStream",
    "BarStream",
    "StreamStatus",
    "Heartbeat",
    "StreamErrorResponse",
    "MarketFlags",
    # Models (Accounts / Balances)
    "AccountSummary",
    "BalanceDetail",
    "AccountBalancesResponse",
    "BODBalance",
    "BODBalancesResponse",
    "AccountsListResponse",
    # Models (Positions)
    "PositionResponse",
    "PositionsResponse",
    # Models (Quotes REST)
    "QuoteSnapshot",
    "QuotesResponse",
    # Mappers
    "normalize_account",
    "normalize_account_balances",
    "normalize_bod_balance",
    "normalize_balances",
    "normalize_execution",
    "normalize_order",
    "normalize_position",
    "normalize_quote",
    # Version
    "__version__",
]
