# TradeStation SDK - Production Deployment Guide

## About This Document

This is a **step-by-step production deployment guide** for deploying trading bots using this SDK. Includes deployment checklists, cloud platform guides, monitoring setup, and critical warnings about LIVE trading.

**Use this if:** You're ready to deploy to production, need cloud deployment instructions, or want deployment best practices.

**⚠️ Critical:** Read **[LIMITATIONS.md](LIMITATIONS.md)** and **[SECURITY.md](SECURITY.md)** before deploying to production.

**Related Documents:**
- 🔒 **[SECURITY.md](SECURITY.md)** - Security best practices (essential before deployment)
- ⚠️ **[LIMITATIONS.md](LIMITATIONS.md)** - Known constraints (review before production)
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Development setup
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history and breaking changes

---

Step-by-step guide for deploying trading bots using this SDK to production environments.

---

## ⚠️ Critical Warnings

**Before deploying to production:**

1. ⚠️ **LIVE mode uses real money** - One mistake can cost thousands
2. ⚠️ **Test thoroughly in PAPER mode first** - At least 1-2 weeks
3. ⚠️ **Implement risk management** - Stop-losses, position limits, kill switches
4. ⚠️ **Monitor continuously** - Don't deploy and forget
5. ⚠️ **Have a rollback plan** - Be ready to shut down immediately

**Never deploy:**
- Untested code
- Without stop-losses
- Without monitoring
- Without understanding LIMITATIONS.md
- On Friday (can't monitor over weekend)

---

## Pre-Deployment Checklist

### Testing & Validation

- [ ] **PAPER mode testing** - At least 1 week of successful paper trading
- [ ] **Error handling** - All error scenarios tested and handled
- [ ] **Edge cases** - Symbol not found, rate limits, network failures tested
- [ ] **Stop-losses** - Verified stop-loss orders work correctly
- [ ] **Position limits** - Max position size enforced
- [ ] **Order limits** - Max orders/day enforced
- [ ] **Logging** - Comprehensive logging to file and/or database
- [ ] **Monitoring** - Alerts set up for errors, unusual activity

### Security

- [ ] **Credentials** - Using environment variables (not .env files)
- [ ] **Secrets management** - AWS Secrets Manager, Azure Key Vault, etc.
- [ ] **Token security** - File permissions set (chmod 600)
- [ ] **No hardcoded secrets** - All credentials from environment
- [ ] **HTTPS only** - SDK enforces, but verify
- [ ] **Audit logging** - All trades logged to audit trail
- [ ] **Read SECURITY.md** - Security best practices implemented

### Infrastructure

- [ ] **Server provisioned** - Adequate CPU, RAM, network
- [ ] **Python 3.10+** - Correct Python version installed
- [ ] **Dependencies installed** - All required packages
- [ ] **Monitoring setup** - Uptime monitoring, log aggregation
- [ ] **Backup plan** - How to restore if server fails
- [ ] **Failover** - Secondary server or manual takeover process

---

## Deployment Environments

### Option 1: Linux Server (Recommended)

**Pros:**
- Stable, reliable
- Easy automation (systemd, cron)
- Good for 24/7 bots

**Setup:**

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Python 3.10+
sudo apt install python3.10 python3.10-venv python3-pip

# 3. Create bot user (security)
sudo useradd -m -s /bin/bash tradingbot

# 4. Set up bot directory
sudo -u tradingbot mkdir -p /home/tradingbot/bot
sudo -u tradingbot chown tradingbot:tradingbot /home/tradingbot/bot

# 5. Install SDK
sudo -u tradingbot python3.10 -m venv /home/tradingbot/bot/.venv
sudo -u tradingbot /home/tradingbot/bot/.venv/bin/pip install tradestation-python-sdk

# 6. Copy bot code
sudo cp my_bot.py /home/tradingbot/bot/
sudo chown tradingbot:tradingbot /home/tradingbot/bot/my_bot.py

# 7. Set up environment variables (via secrets manager)
# See "Environment Variables" section below
```

---

### Option 2: Docker Container

**Pros:**
- Portable, consistent
- Easy to version and rollback
- Isolated from host system

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install SDK
RUN pip install --no-cache-dir tradestation-python-sdk

# Copy bot code
COPY my_bot.py /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Run as non-root user
RUN useradd -m -u 1000 tradingbot && chown -R tradingbot:tradingbot /app
USER tradingbot

# Set environment variables (will be overridden by docker run)
ENV TRADING_MODE=PAPER

# Run bot
CMD ["python", "my_bot.py"]
```

**Build and run:**

```bash
# Build image
docker build -t my-trading-bot:1.0.0 .

# Run with environment file
docker run --env-file .env.production my-trading-bot:1.0.0

# Or with secrets
docker run \
  -e TRADESTATION_CLIENT_ID=$CLIENT_ID \
  -e TRADESTATION_CLIENT_SECRET=$CLIENT_SECRET \
  -e TRADING_MODE=LIVE \
  my-trading-bot:1.0.0
```

---

### Option 3: Cloud Platforms

#### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 22.04 LTS)
# Instance type: t3.micro or larger

# 2. SSH into instance
ssh -i your-key.pem ubuntu@ec2-instance-ip

# 3. Install dependencies
sudo apt update
sudo apt install python3.10 python3.10-venv

# 4. Clone and setup
git clone https://github.com/yourusername/your-bot.git
cd your-bot
python3.10 -m venv .venv
source .venv/bin/activate
pip install tradestation-python-sdk

# 5. Set up AWS Secrets Manager
aws secretsmanager create-secret \
  --name trading-bot-credentials \
  --secret-string '{"CLIENT_ID":"...","CLIENT_SECRET":"..."}'

# 6. Update bot to read from Secrets Manager
# (See "AWS Secrets Manager" section below)
```

#### Google Cloud (GCP)

```bash
# 1. Create Compute Engine instance
gcloud compute instances create trading-bot \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud

# 2. SSH and setup
gcloud compute ssh trading-bot
# Follow same steps as AWS EC2

# 3. Use Secret Manager
gcloud secrets create trading-bot-credentials \
  --data-file=credentials.json
```

#### Azure

```bash
# 1. Create VM
az vm create \
  --resource-group trading-bots \
  --name trading-bot-1 \
  --image Ubuntu2204 \
  --size Standard_B1s

# 2. SSH and setup
# Follow same steps as AWS EC2

# 3. Use Azure Key Vault
az keyvault secret set \
  --vault-name trading-vault \
  --name client-id \
  --value "your-client-id"
```

---

## Environment Variables (Production)

### Don't Use .env Files in Production

**❌ Bad (Development only):**
```bash
# .env file
TRADESTATION_CLIENT_ID=abc123
```

**✅ Good (Production):**

#### Option 1: Export in Shell

```bash
# In systemd service file or startup script
export TRADESTATION_CLIENT_ID="abc123"
export TRADESTATION_CLIENT_SECRET="xyz789"
export TRADING_MODE="LIVE"
```

#### Option 2: AWS Secrets Manager

```python
import boto3
import json

def get_credentials():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='trading-bot-credentials')
    secrets = json.loads(response['SecretString'])
    
    os.environ['TRADESTATION_CLIENT_ID'] = secrets['CLIENT_ID']
    os.environ['TRADESTATION_CLIENT_SECRET'] = secrets['CLIENT_SECRET']
    os.environ['TRADING_MODE'] = secrets['TRADING_MODE']

# Call before initializing SDK
get_credentials()
sdk = TradeStationSDK()
```

#### Option 3: Azure Key Vault

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_credentials():
    credential = DefaultAzureCredential()
    client = SecretClient(
        vault_url="https://trading-vault.vault.azure.net/",
        credential=credential
    )
    
    os.environ['TRADESTATION_CLIENT_ID'] = client.get_secret('client-id').value
    os.environ['TRADESTATION_CLIENT_SECRET'] = client.get_secret('client-secret').value
    os.environ['TRADING_MODE'] = client.get_secret('trading-mode').value

get_credentials()
sdk = TradeStationSDK()
```

---

## Process Management

### Systemd Service (Linux)

**Create service file: `/etc/systemd/system/trading-bot.service`**

```ini
[Unit]
Description=Trading Bot using TradeStation SDK
After=network.target

[Service]
Type=simple
User=tradingbot
WorkingDirectory=/home/tradingbot/bot
ExecStart=/home/tradingbot/bot/.venv/bin/python /home/tradingbot/bot/main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Environment variables (use secrets manager instead)
# Environment="TRADING_MODE=LIVE"

[Install]
WantedBy=multi-user.target
```

**Enable and start:**

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (start on boot)
sudo systemctl enable trading-bot

# Start service
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot

# View logs
sudo journalctl -u trading-bot -f
```

---

### Supervisor (Alternative)

**Install supervisor:**

```bash
sudo apt install supervisor
```

**Create config: `/etc/supervisor/conf.d/trading-bot.conf`**

```ini
[program:trading-bot]
command=/home/tradingbot/bot/.venv/bin/python /home/tradingbot/bot/main.py
directory=/home/tradingbot/bot
user=tradingbot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/trading-bot.log
```

**Start:**

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start trading-bot
```

---

## Monitoring & Alerting

### Log Aggregation

**Send logs to centralized system:**

```python
import logging
from logging.handlers import SysLogHandler

# Send to syslog (Papertrail, Loggly, etc.)
handler = SysLogHandler(address=('logs.papertrailapp.com', 12345))
logging.getLogger().addHandler(handler)
```

### Health Checks

**Create health check endpoint:**

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    try:
        # Check SDK is working
        info = sdk.info()
        account = sdk.get_account_info(mode="LIVE")
        
        return jsonify({
            "status": "healthy",
            "sdk_version": info['version'],
            "authenticated": "LIVE" in info['authenticated_modes'],
            "account_id": account.get('account_id')
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
```

**Monitor with uptime service:**
- UptimeRobot
- Pingdom
- AWS CloudWatch
- Custom monitoring

---

### Alerting

**Send alerts on errors:**

```python
import smtplib
from email.message import EmailMessage

def send_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'bot@example.com'
    msg['To'] = 'admin@example.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('bot@example.com', 'password')
        smtp.send_message(msg)

# Use in bot
try:
    order_id, status = sdk.place_order(...)
except TradeStationAPIError as e:
    send_alert("Trading Bot Error", f"Order failed: {e}")
    raise
```

**Alerting services:**
- PagerDuty
- Twilio (SMS)
- Slack webhooks
- Discord webhooks
- Email (SMTP)

---

## Backup & Recovery

### Token Backup

**Backup token files regularly:**

```bash
# Backup tokens
cp logs/tokens_live.json backups/tokens_live_$(date +%Y%m%d).json

# Or sync to S3
aws s3 cp logs/tokens_live.json s3://my-bucket/backups/
```

### State Backup

**Save bot state:**

```python
import json
from datetime import datetime

def save_state(positions, orders, balances):
    state = {
        "timestamp": datetime.now().isoformat(),
        "positions": positions,
        "orders": orders,
        "balances": balances
    }
    
    with open(f"state_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        json.dump(state, f, indent=2)
```

### Disaster Recovery

**If server fails:**

1. **Stop all trading** - Cancel all open orders
2. **Assess damage** - Check positions, balances, order history
3. **Restore to new server** - Deploy to backup server
4. **Verify state** - Confirm positions and orders match
5. **Resume trading** - Only after verification

**Failover script:**

```python
# emergency_shutdown.py
from tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="LIVE")

# Cancel all orders
sdk.cancel_all_orders(mode="LIVE")
print("✅ All orders cancelled")

# Flatten all positions
sdk.flatten_position(mode="LIVE")
print("✅ All positions closed")

# Get final state
balances = sdk.get_account_balances(mode="LIVE")
print(f"Final balance: ${balances['equity']:,.2f}")
```

---

## Performance Optimization

### Connection Reuse

**Current (v1.x):**
```python
# Each request creates new connection
for symbol in symbols:
    quote = sdk.get_quote_snapshots(symbol, mode="LIVE")
```

**Optimized (batch requests):**
```python
# Single request for multiple symbols
symbols_str = ",".join(symbols)
quotes = sdk.get_quote_snapshots(symbols_str, mode="LIVE")
```

### Rate Limit Management

**Implement request throttling:**

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_requests=60, window=60):
        self.max_requests = max_requests
        self.window = window
        self.requests = deque()
    
    def wait_if_needed(self):
        now = time.time()
        
        # Remove old requests outside window
        while self.requests and self.requests[0] < now - self.window:
            self.requests.popleft()
        
        # Check if at limit
        if len(self.requests) >= self.max_requests:
            sleep_time = self.window - (now - self.requests[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        
        self.requests.append(now)

# Usage
limiter = RateLimiter(max_requests=60, window=60)

for symbol in symbols:
    limiter.wait_if_needed()
    quote = sdk.get_quote_snapshots(symbol, mode="LIVE")
```

---

## Scaling Strategies

### Horizontal Scaling (Multiple Bots)

**Run multiple strategies on separate servers:**

```
Strategy A → Server 1 → Account 1
Strategy B → Server 2 → Account 2
Strategy C → Server 3 → Account 3
```

**Benefits:**
- Isolation (one strategy failure doesn't affect others)
- Better resource utilization
- Can use different accounts/brokers

### Vertical Scaling (Multiple Strategies, One Server)

**Run multiple strategies on one server:**

```python
import asyncio

async def run_strategy_a():
    sdk = TradeStationSDK()
    sdk.authenticate(mode="LIVE")
    # Strategy A logic

async def run_strategy_b():
    sdk = TradeStationSDK()
    sdk.authenticate(mode="LIVE")
    # Strategy B logic

async def main():
    await asyncio.gather(
        run_strategy_a(),
        run_strategy_b()
    )

asyncio.run(main())
```

---

## Cost Optimization

### Reduce API Calls

**Use streaming instead of polling:**

```python
# ❌ Expensive: Poll every second (60+ API calls/minute)
while True:
    quote = sdk.get_quote_snapshots("AAPL", mode="LIVE")
    time.sleep(1)

# ✅ Cheap: Stream (1 connection, unlimited updates)
async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="LIVE"):
    process_quote(quote)
```

### Optimize Server Costs

**Right-size your server:**

| Bot Type | CPU | RAM | Network | Cost/Month |
|----------|-----|-----|---------|------------|
| Simple strategy | 1 vCPU | 1GB | Low | $5-10 |
| Multi-strategy | 2 vCPU | 2GB | Medium | $20-40 |
| High-frequency | 4+ vCPU | 8GB+ | High | $100+ |

**Recommendations:**
- Start small (t3.micro on AWS)
- Monitor resource usage
- Scale up only if needed
- Use spot instances for dev/testing

---

## Regulatory & Compliance

### Logging Requirements

**Maintain audit trail:**

```python
import logging

# Set up audit logger
audit_logger = logging.getLogger('audit')
audit_handler = logging.FileHandler('audit.log')
audit_logger.addHandler(audit_handler)

def place_order_audited(symbol, side, quantity, **kwargs):
    # Log before placing
    audit_logger.info(f"ORDER_INTENT: {symbol} {side} {quantity} {kwargs}")
    
    try:
        order_id, status = sdk.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            **kwargs
        )
        
        # Log success
        audit_logger.info(f"ORDER_PLACED: {order_id} {status}")
        return order_id, status
        
    except Exception as e:
        # Log failure
        audit_logger.error(f"ORDER_FAILED: {e}")
        raise
```

**Keep logs for:**
- At least 7 years (SEC requirement for some traders)
- Include: timestamp, symbol, side, quantity, price, order ID, status

### Pattern Day Trader Rules

**If trading stocks:**
- Must maintain $25,000 minimum equity
- Limited to 3 day trades per 5 days (if below $25k)
- SDK doesn't enforce PDT rules - you must implement

**Check before trading:**

```python
def can_day_trade(sdk):
    balances = sdk.get_account_balances(mode="LIVE")
    equity = balances['equity']
    
    if equity < 25000:
        # Check day trades in last 5 days
        orders = sdk.get_order_history(
            start_date=(datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            mode="LIVE"
        )
        day_trades = count_day_trades(orders)
        
        if day_trades >= 3:
            return False
    
    return True
```

---

## Rollout Strategy

### Phase 1: Testing (Week 1-2)

- Deploy to staging server
- Test with PAPER mode
- Verify all features work
- Monitor logs for errors
- Run for 1-2 weeks

### Phase 2: Pilot (Week 3)

- Switch to LIVE mode
- **Start with $100-500 position sizes**
- Monitor 24/7
- Be ready to shut down
- Check every 2-4 hours

### Phase 3: Limited Production (Week 4-6)

- Increase to $1,000-5,000 position sizes
- Monitor daily
- Refine based on performance
- Document any issues

### Phase 4: Full Production (Week 7+)

- Increase to full position sizes
- Automated monitoring
- Weekly reviews
- Continuous improvement

**Never skip phases!** Each phase catches different issues.

---

## Maintenance

### Daily Tasks

- [ ] Check bot is running (`systemctl status trading-bot`)
- [ ] Review logs for errors
- [ ] Verify positions match expectations
- [ ] Check P&L

### Weekly Tasks

- [ ] Review trading performance
- [ ] Check for SDK updates (`pip list --outdated`)
- [ ] Review error logs for patterns
- [ ] Backup token files and state

### Monthly Tasks

- [ ] Rotate credentials (if policy requires)
- [ ] Review and optimize strategies
- [ ] Update dependencies
- [ ] Disaster recovery drill

---

## Support & Escalation

### If Something Goes Wrong

**Severity Levels:**

**P0 - Critical (Immediate Action):**
- Bot placing orders incorrectly
- Positions not closing
- Security breach

**Actions:**
1. Run emergency shutdown script
2. Investigate logs
3. Fix issue
4. Test fix in PAPER mode
5. Redeploy

**P1 - High (1-hour response):**
- Bot stopped working
- Orders not filling
- Streaming disconnected

**Actions:**
1. Check logs
2. Restart bot
3. Monitor for recurrence

**P2 - Medium (Same day):**
- Performance degradation
- Non-critical errors
- Warning messages

**P3 - Low (Next week):**
- Feature requests
- Documentation improvements
- Optimization opportunities

---

## Checklist Before Going Live

- [ ] Read this entire document
- [ ] Read [SECURITY.md](SECURITY.md)
- [ ] Read [LIMITATIONS.md](LIMITATIONS.md)
- [ ] Tested in PAPER mode (1+ weeks)
- [ ] Implemented all error handling
- [ ] Set up monitoring and alerts
- [ ] Configured secrets manager
- [ ] Created emergency shutdown script
- [ ] Documented rollback procedure
- [ ] Configured automatic backups
- [ ] Set up audit logging
- [ ] Tested with small positions first
- [ ] Have 24/7 monitoring plan
- [ ] Know how to contact support

**Only check this box when 100% ready:** [ ] Ready for production

---

## Resources

- 🔒 [SECURITY.md](SECURITY.md) - Security best practices
- ⚠️ [LIMITATIONS.md](LIMITATIONS.md) - Known constraints
- 📖 [README.md](README.md) - Main documentation
- 💬 [Get Help](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

**Remember: Trading involves risk. Deploy responsibly.** ⚠️

---

**Last Updated:** 2025-12-07  
**SDK Version:** 1.0.0
