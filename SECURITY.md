# TradeStation SDK - Security Guide

## About This Document

This is a **comprehensive security guide** covering best practices, credential management, token security, and production deployment security considerations. Essential reading before deploying to production.

**Use this if:** You're deploying to production, handling credentials, or want to ensure secure SDK usage.

**Related Documents:**
- 🚀 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide (includes security checklist)
- ⚠️ **[LIMITATIONS.md](LIMITATIONS.md)** - Security limitations (token storage, encryption)
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 🔄 **[MIGRATION.md](MIGRATION.md)** - Security considerations when migrating
- 📦 **[INSTALLATION.md](INSTALLATION.md)** - Secure installation practices

---

Best practices and security considerations when using the TradeStation SDK.

---

## 🔒 Critical Security Principles

### Production Hardening (new defaults)

- **OAuth callback surface:** Callback server now binds to `127.0.0.1` only. Keep redirect URIs on loopback; refuse public hosts.
- **CSRF/state:** SDK generates a per-auth cryptographically random `state` and validates it on callback. Do not disable.
- **Token files:** Token JSON files are saved with `chmod 600` (owner-only). Confirm permissions on first run, especially on shared systems.
- **Logging:** Even if `TRADESTATION_FULL_LOGGING` is set, `ENVIRONMENT=prod|production` forces full logging **off**, and sensitive endpoints (auth/token/orderexecution/orders) never log bodies.
- **Action items for prod:**
  - Set `ENVIRONMENT=production` in your runtime.
  - Keep `TRADESTATION_FULL_LOGGING` unset in prod; use it only locally.
  - Verify token files are owner-only (`ls -l config/tokens_*.json` → `-rw-------`).
  - Ensure redirect URI host is loopback (localhost/127.0.0.1); rotate client secrets if exposed.
  - Prefer a secrets manager for CLIENT_SECRET and consider encrypted token storage (see “Planned Improvement” below).

### 1. Never Commit Credentials

**Never commit these files:**
- ❌ `.env` - Contains API credentials
- ❌ `logs/tokens_*.json` - Contains access/refresh tokens
- ❌ Any file with `CLIENT_SECRET` or `ACCESS_TOKEN`

**Always commit:**
- ✅ `.env.example` - Template without credentials
- ✅ `.gitignore` - Excludes sensitive files

**Verify .gitignore includes:**
```gitignore
.env
.env.local
.env.*.local
logs/
*.log
tokens_*.json
```

---

### 2. Secure Token Storage

**Current Implementation:**
- Tokens stored as plain JSON in `logs/tokens_*.json`
- **Not encrypted at rest**
- Requires file system protection

**Secure Your Token Files:**

**On Linux/macOS:**
```bash
# Set restrictive permissions (owner read/write only)
chmod 600 logs/tokens_*.json
chmod 700 logs/

# Verify permissions
ls -la logs/tokens_*.json
# Should show: -rw------- (600)
```

**On Windows:**
```powershell
# Remove inheritance and set owner-only access
icacls logs\tokens_paper.json /inheritance:r
icacls logs\tokens_paper.json /grant:r "%USERNAME%:(R,W)"
```

**Planned Improvement (v1.1):**
- System keychain integration
- Encrypted token storage
- No plain-text tokens on disk

**Custom Encryption (Advanced):**
```python
from cryptography.fernet import Fernet
import json

class EncryptedTokenManager(TokenManager):
    def __init__(self, *args, encryption_key=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cipher = Fernet(encryption_key or Fernet.generate_key())
    
    def save_tokens(self, mode, tokens):
        encrypted = self.cipher.encrypt(json.dumps(tokens).encode())
        # Save encrypted tokens
```

---

### 3. Environment Variable Security

**Use .env files for local development:**
```env
TRADESTATION_CLIENT_ID=abc123
TRADESTATION_CLIENT_SECRET=xyz789
```

**Use environment variables in production:**
```bash
# Export via shell (temporary)
export TRADESTATION_CLIENT_ID=abc123

# Or use secrets management (preferred)
# AWS Secrets Manager, Azure Key Vault, etc.
```

**Never hardcode credentials:**
```python
# ❌ Bad - hardcoded credentials
sdk = TradeStationSDK()
sdk.client_id = "abc123"  # DON'T DO THIS

# ✅ Good - from environment
sdk = TradeStationSDK()  # Reads from .env
```

---

## 🛡️ API Security Best Practices

### 4. Start with PAPER Mode

**Always test with PAPER mode first:**

```python
# ✅ Safe for testing
sdk.authenticate(mode="PAPER")
sdk.place_order(..., mode="PAPER")

# ⚠️ Only use LIVE mode in production after thorough testing
sdk.authenticate(mode="LIVE")
sdk.place_order(..., mode="LIVE")
```

**Why?**
- PAPER mode uses simulator (no real money)
- Test strategies without risk
- Verify code works before going live

---

### 5. Validate Inputs

**Always validate order parameters:**

```python
def place_order_safe(symbol, side, quantity, price):
    # Validate symbol
    if not symbol or len(symbol) < 1:
        raise ValueError("Invalid symbol")
    
    # Validate side
    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    
    # Validate quantity
    if quantity <= 0:
        raise ValueError("Quantity must be positive")
    
    # Validate price
    if price <= 0:
        raise ValueError("Price must be positive")
    
    # Place order
    return sdk.place_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        limit_price=price,
        mode="PAPER"
    )
```

**Why?**
- Prevent accidental invalid orders
- Catch errors before API call
- Save API rate limit quota

---

### 6. Implement Order Limits

**Prevent runaway trading:**

```python
class TradingLimits:
    def __init__(self, max_orders_per_day=100, max_position_size=10):
        self.max_orders_per_day = max_orders_per_day
        self.max_position_size = max_position_size
        self.orders_today = 0
    
    def can_place_order(self, quantity):
        # Check daily order limit
        if self.orders_today >= self.max_orders_per_day:
            raise Exception(f"Daily order limit reached ({self.max_orders_per_day})")
        
        # Check position size limit
        if quantity > self.max_position_size:
            raise Exception(f"Position size exceeds limit ({self.max_position_size})")
        
        return True
    
    def record_order(self):
        self.orders_today += 1

# Usage
limits = TradingLimits(max_orders_per_day=50, max_position_size=5)

if limits.can_place_order(quantity=2):
    order_id, status = sdk.place_order(...)
    limits.record_order()
```

---

### 7. Log All Operations

**Maintain audit trail:**

```python
import logging

# Configure logging
logging.basicConfig(
    filename='trading_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def place_order_logged(symbol, side, quantity, **kwargs):
    # Log before placing
    logging.info(f"Placing order: {symbol} {side} {quantity}")
    
    try:
        order_id, status = sdk.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            **kwargs
        )
        # Log success
        logging.info(f"Order placed successfully: {order_id}")
        return order_id, status
    except Exception as e:
        # Log failure
        logging.error(f"Order failed: {e}")
        raise
```

---

## 🔐 Production Security Checklist

Before deploying to production:

- [ ] **Credentials:**
  - [ ] Use environment variables (not .env files)
  - [ ] Use secrets management (AWS Secrets Manager, etc.)
  - [ ] Rotate credentials regularly (every 90 days)
  - [ ] Never log credentials or tokens

- [ ] **Token Security:**
  - [ ] Set restrictive file permissions (600)
  - [ ] Encrypt token storage (custom implementation or wait for v1.1)
  - [ ] Monitor token expiration and refresh
  - [ ] Revoke old tokens when rotating credentials

- [ ] **Network Security:**
  - [ ] Use HTTPS only (SDK enforces this)
  - [ ] Verify TLS certificates
  - [ ] Use VPN for sensitive operations
  - [ ] Whitelist API endpoints in firewall

- [ ] **Application Security:**
  - [ ] Implement rate limiting
  - [ ] Validate all inputs
  - [ ] Set order limits (max quantity, max orders/day)
  - [ ] Implement circuit breakers
  - [ ] Log all trading operations
  - [ ] Monitor for unusual activity

- [ ] **Access Control:**
  - [ ] Limit who can access production credentials
  - [ ] Use separate credentials for dev/staging/prod
  - [ ] Implement least-privilege principle
  - [ ] Audit access logs regularly

- [ ] **Testing:**
  - [ ] Test thoroughly in PAPER mode first
  - [ ] Test error handling and edge cases
  - [ ] Test with small positions in LIVE mode
  - [ ] Monitor for 24-48 hours before full deployment

---

## 🚨 Incident Response

### If Credentials Are Compromised

1. **Immediately revoke credentials:**
   - Go to TradeStation Developer Portal
   - Delete the compromised application
   - Create new application with new credentials

2. **Check for unauthorized activity:**
   - Review order history
   - Check account balances
   - Look for unexpected trades

3. **Update all systems:**
   - Update .env files
   - Re-authenticate SDK
   - Rotate all related credentials

4. **Post-mortem:**
   - How were credentials compromised?
   - What can be done to prevent recurrence?
   - Update security procedures

---

### If Tokens Are Compromised

1. **Tokens expire in 20 minutes** (access tokens)
2. **Refresh tokens are long-lived** - if compromised:
   - Re-authenticate to get new refresh token
   - Old refresh token is invalidated
   - Monitor account for unauthorized activity

3. **Delete token files:**
   ```bash
   rm logs/tokens_*.json
   sdk.authenticate(mode="PAPER")  # Re-authenticate
   ```

---

## 🔍 Security Monitoring

### Monitor These Indicators

**Warning Signs:**
- Unexpected orders in order history
- Balance changes you didn't make
- Failed authentication attempts
- Unusual API activity patterns
- Rate limit errors (may indicate credential theft/abuse)

**Monitoring Script:**
```python
def check_security_indicators(sdk):
    """Check for unusual activity."""
    # Get recent orders
    orders = sdk.get_order_history(limit=100, mode="LIVE")
    
    # Check for orders you didn't place
    for order in orders:
        # Your validation logic here
        pass
    
    # Get balance changes
    balances = sdk.get_account_balances(mode="LIVE")
    # Compare with expected balances
    
    # Log any anomalies
    pass
```

---

## 📚 Additional Resources

- [TradeStation Security Best Practices](https://www.tradestation.com/security)
- [OAuth 2.0 Security](https://oauth.net/2/security-considerations/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

## Reporting Security Issues

**Found a security vulnerability in the SDK?**

**Please DO NOT open a public issue.**

Instead:
1. Email: security@example.com
2. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if known)

We'll respond within 48 hours and work with you to fix the issue before public disclosure.

---

**Security is everyone's responsibility. Stay safe!** 🔒
