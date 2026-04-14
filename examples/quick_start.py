#!/usr/bin/env python3
"""
TradeStation SDK - Quick Start Example

A simple script demonstrating basic SDK usage:
- Authentication
- Account information
- Account balances
- Placing a simple order (commented out for safety)

This is a standalone example that works independently of the trading bot.
"""

import os

from dotenv import load_dotenv
from tradestation import AuthenticationError, TradeStationSDK


def main():
    """Run quick start example."""
    print("=" * 60)
    print("TradeStation SDK - Quick Start Example")
    print("=" * 60)
    print()

    # Load environment variables
    load_dotenv()

    # Verify credentials
    if not os.getenv("TRADESTATION_CLIENT_ID"):
        print("❌ Error: TRADESTATION_CLIENT_ID not set in environment")
        print("   Create a .env file with your credentials")
        return 1

    # Initialize SDK
    print("📦 Initializing SDK...")
    sdk = TradeStationSDK()

    # Get SDK info
    info = sdk.info()
    print(f"✅ SDK v{info['version']} initialized")
    print(f"   API Version: {info['api_version']}")
    print(f"   Features: {', '.join(info['features'].keys())}")
    print()

    # Authenticate
    print("🔐 Authenticating with TradeStation (PAPER mode)...")
    try:
        sdk.authenticate(mode="PAPER")
        print("✅ Authentication successful")
        print()
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return 1

    # Get account information
    print("👤 Fetching account information...")
    try:
        account = sdk.get_account_info(mode="PAPER")
        print(f"✅ Account: {account['account_id']}")
        print(f"   Name: {account['name']}")
        print(f"   Type: {account['type']}")
        print(f"   Status: {account['status']}")
        print()
    except Exception as e:
        print(f"❌ Failed to get account info: {e}")
        return 1

    # Get account balances
    print("💰 Fetching account balances...")
    try:
        balances = sdk.get_account_balances(mode="PAPER")
        print(f"✅ Equity: ${balances['equity']:,.2f}")
        print(f"   Cash Balance: ${balances['cash_balance']:,.2f}")
        print(f"   Buying Power: ${balances['buying_power']:,.2f}")
        print(f"   Margin Available: ${balances['margin_available']:,.2f}")
        print(f"   Open P&L: ${balances['open_pnl']:,.2f}")
        print()
    except Exception as e:
        print(f"❌ Failed to get balances: {e}")
        return 1

    # Example: Place an order (commented out for safety)
    print("📝 Order Placement Example (commented out for safety)")
    print("   Uncomment the code below to place a test order:")
    print()
    print("   # Place a limit order for AAPL")
    print("   order_id, status = sdk.place_limit_order(")
    print("       symbol='AAPL',")
    print("       side='BUY',")
    print("       quantity=10,")
    print("       limit_price=150.00,")
    print("       mode='PAPER'")
    print("   )")
    print("   print(f'Order placed: {order_id}')")
    print()

    # Summary
    print("=" * 60)
    print("✅ Quick Start Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  📖 Check out the Jupyter notebooks in examples/")
    print("  💡 Read the complete documentation in docs/")
    print("  🔧 Explore advanced examples in docs/SDK_USAGE_EXAMPLES.md")
    print()

    return 0


if __name__ == "__main__":
    exit(main())
