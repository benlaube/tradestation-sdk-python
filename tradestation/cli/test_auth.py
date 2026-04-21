#!/usr/bin/env python3
"""
TradeStation SDK Authentication Test

Quick test to verify SDK authentication works.

Usage:
    python test_auth.py PAPER
    python test_auth.py LIVE
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from tradestation import AuthenticationError, TradeStationSDK


def test_authentication(mode="PAPER"):
    """
    Test SDK authentication.

    Args:
        mode: Trading mode ("PAPER" or "LIVE")

    Returns:
        True if successful, False otherwise
    """
    print("=" * 60)
    print(f"TradeStation SDK Authentication Test - {mode} Mode")
    print("=" * 60)
    print()

    # Load environment variables
    load_dotenv()

    # Verify credentials
    if not os.getenv("TRADESTATION_CLIENT_ID"):
        print("❌ Error: TRADESTATION_CLIENT_ID not set")
        print("   Create a .env file with your credentials")
        return False

    print("📦 Initializing SDK...")
    sdk = TradeStationSDK()

    # Get SDK info
    info = sdk.info()
    print(f"✅ SDK v{info['version']} initialized")
    print()

    print(f"🔐 Testing authentication for {mode} mode...")

    try:
        # Authenticate
        sdk.authenticate(mode=mode)
        print("✅ Authentication successful")
        print()

        # Get account info
        print("👤 Fetching account information...")
        account = sdk.get_account_info(mode=mode)
        print(f"✅ Connected to account: {account['account_id']}")
        print(f"   Name: {account['name']}")
        print(f"   Type: {account['type']}")
        print()

        # Get balances
        print("💰 Fetching account balances...")
        balances = sdk.get_account_balances(mode=mode)
        print(f"✅ Equity: ${balances['equity']:,.2f}")
        print(f"   Buying Power: ${balances['buying_power']:,.2f}")
        print()

        # Verify token
        print("🔑 Verifying token...")
        sdk.ensure_authenticated(mode=mode)
        print("✅ Token is valid")
        print()

        print("=" * 60)
        print("✅ Authentication test PASSED")
        print("=" * 60)
        return True

    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Verify credentials in .env file")
        print("  2. Check redirect URI matches (http://localhost:8888/callback)")
        print("  3. Ensure port 8888 is available")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Main entry point."""
    # Get mode from command line
    mode = sys.argv[1] if len(sys.argv) > 1 else "PAPER"

    # Validate mode
    if mode not in ["PAPER", "LIVE"]:
        print(f"❌ Invalid mode: {mode}")
        print("   Usage: python test_auth.py [PAPER|LIVE]")
        return 1

    # Warn for LIVE mode
    if mode == "LIVE":
        print("⚠️  WARNING: Testing LIVE mode authentication")
        print("⚠️  This will connect to your LIVE trading account")
        print()
        response = input("   Continue? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Aborted")
            return 1
        print()

    # Run test
    success = test_authentication(mode)
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
