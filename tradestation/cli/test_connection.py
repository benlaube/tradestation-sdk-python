#!/usr/bin/env python3
"""
TradeStation SDK Comprehensive Connection Test

Tests all major SDK components:
- Authentication
- Account operations
- Market data
- Order queries (no actual orders placed)

Usage:
    python test_connection.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from tradestation import TradeStationSDK


def print_section(title):
    """Print a section header."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)
    print()


def test_authentication(sdk, mode):
    """Test authentication."""
    print("🔐 Testing authentication...")
    try:
        sdk.authenticate(mode=mode)
        print("✅ Authentication successful")
        return True
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False


def test_account_info(sdk, mode):
    """Test account information retrieval."""
    print("👤 Testing account information...")
    try:
        account = sdk.get_account_info(mode=mode)
        print(f"✅ Account ID: {account['account_id']}")
        print(f"   Name: {account['name']}")
        print(f"   Type: {account['type']}")
        print(f"   Status: {account['status']}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_account_balances(sdk, mode):
    """Test balance retrieval."""
    print("💰 Testing account balances...")
    try:
        balances = sdk.get_account_balances(mode=mode)
        print(f"✅ Equity: ${balances['equity']:,.2f}")
        print(f"   Cash Balance: ${balances['cash_balance']:,.2f}")
        print(f"   Buying Power: ${balances['buying_power']:,.2f}")
        print(f"   Margin Available: ${balances['margin_available']:,.2f}")
        print(f"   Open P&L: ${balances['open_pnl']:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_market_data(sdk, mode):
    """Test market data retrieval."""
    print("📊 Testing market data...")

    # Test symbol search
    print("  • Symbol search...")
    try:
        symbols = sdk.search_symbols(pattern="AAPL", category="Stock", mode=mode)
        if symbols:
            print(f"    ✅ Found {len(symbols)} symbol(s)")
        else:
            print("    ⚠️  No symbols found")
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False

    # Test quote snapshots
    print("  • Quote snapshots...")
    try:
        quotes = sdk.get_quote_snapshots("AAPL", mode=mode)
        if quotes.get("Quotes"):
            quote = quotes["Quotes"][0]
            print(
                f"    ✅ AAPL: Last=${quote.get('Last', 'N/A')}, Bid=${quote.get('Bid', 'N/A')}, Ask=${quote.get('Ask', 'N/A')}"
            )
        else:
            print("    ⚠️  No quotes returned")
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False

    # Test historical bars
    print("  • Historical bars...")
    try:
        bars = sdk.get_bars("AAPL", "1", "Minute", 10, mode=mode)
        if bars:
            print(f"    ✅ Retrieved {len(bars)} bars")
        else:
            print("    ⚠️  No bars returned")
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False

    print("✅ Market data tests passed")
    return True


def test_order_queries(sdk, mode):
    """Test order query operations (no actual orders placed)."""
    print("📝 Testing order queries...")

    # Test order history
    print("  • Order history...")
    try:
        orders = sdk.get_order_history(limit=10, mode=mode)
        print(f"    ✅ Retrieved {len(orders)} historical order(s)")
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False

    # Test current orders
    print("  • Current orders...")
    try:
        current = sdk.get_current_orders(mode=mode)
        order_count = len(current.get("Orders", []))
        print(f"    ✅ {order_count} current order(s)")
    except Exception as e:
        print(f"    ❌ Failed: {e}")
        return False

    print("✅ Order query tests passed")
    return True


def test_positions(sdk, mode):
    """Test position queries."""
    print("📍 Testing position queries...")
    try:
        positions = sdk.get_all_positions(mode=mode)
        print(f"✅ {len(positions)} position(s) found")
        if positions:
            for pos in positions[:3]:  # Show first 3
                print(f"   • {pos.get('Symbol')}: {pos.get('Quantity')} @ ${pos.get('AveragePrice', 0):.2f}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def main():
    """Run comprehensive connection test."""
    print_section("TradeStation SDK Comprehensive Connection Test")

    # Load environment variables
    load_dotenv()

    # Verify credentials
    if not os.getenv("TRADESTATION_CLIENT_ID"):
        print("❌ Error: TRADESTATION_CLIENT_ID not set")
        print("   Create a .env file with your credentials")
        return 1

    # Get mode
    mode = os.getenv("TRADING_MODE", "PAPER")
    print(f"Testing in {mode} mode")
    print()

    # Initialize SDK
    print("📦 Initializing SDK...")
    sdk = TradeStationSDK()
    info = sdk.info()
    print(f"✅ SDK v{info['version']} initialized")

    # Track results
    results = {}

    # Run tests
    print_section("Test 1: Authentication")
    results["auth"] = test_authentication(sdk, mode)

    if not results["auth"]:
        print()
        print("❌ Authentication failed - cannot continue")
        return 1

    print_section("Test 2: Account Information")
    results["account_info"] = test_account_info(sdk, mode)

    print_section("Test 3: Account Balances")
    results["balances"] = test_account_balances(sdk, mode)

    print_section("Test 4: Market Data")
    results["market_data"] = test_market_data(sdk, mode)

    print_section("Test 5: Order Queries")
    results["order_queries"] = test_order_queries(sdk, mode)

    print_section("Test 6: Position Queries")
    results["positions"] = test_positions(sdk, mode)

    # Summary
    print_section("Test Summary")
    passed = sum(results.values())
    total = len(results)

    print(f"Results: {passed}/{total} tests passed")
    print()
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    print()

    if passed == total:
        print("=" * 60)
        print("🎉 All tests PASSED! SDK is working correctly.")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print(f"⚠️  {total - passed} test(s) FAILED")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    exit(main())
