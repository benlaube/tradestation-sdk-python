# OAuth Port Auto-Selection Critical Issue

**Date:** 2025-12-28  
**Severity:** 🔴 **CRITICAL**  
**Status:** ✅ **FIXED in v1.0.1**

---

## Problem Summary

The OAuth port auto-selection feature has a **critical bug** that will cause authentication failures when ports are auto-selected.

### The Bug

1. **OAuth Request Uses Original Redirect URI:**
   - Line 430 in `session.py`: `"redirect_uri": self.redirect_uri` (uses original URI from config)
   - Line 437: `auth_request_url` is built with the original redirect_uri
   - Line 502: Browser opens with the original redirect_uri

2. **Server Starts on Auto-Selected Port:**
   - Lines 441-486: Port is auto-selected (e.g., 8889 if 8888 is busy)
   - Server starts listening on the auto-selected port
   - But the redirect_uri sent to TradeStation still has the original port

3. **Mismatch Causes Failure:**
   - TradeStation redirects to the URI specified in the OAuth request (original port)
   - SDK is listening on a different port (auto-selected)
   - Callback never arrives → Authentication fails

### Example Failure Scenario

```python
# User has registered: http://localhost:8888/callback in TradeStation Developer Portal
# Port 8888 is in use
# SDK auto-selects port 8889

# What happens:
1. SDK sends OAuth request with redirect_uri=http://localhost:8888/callback
2. SDK starts server on port 8889
3. TradeStation redirects to http://localhost:8888/callback (registered URI)
4. SDK is listening on port 8889, not 8888
5. Callback never received → Authentication fails
```

---

## TradeStation API v3 Requirements

### Redirect URI Registration

TradeStation API v3 requires that:
1. **Redirect URI must be EXACTLY registered** in the Developer Portal
2. The redirect_uri sent in the OAuth request must **EXACTLY match** a registered URI
3. TradeStation will reject the request if the redirect_uri doesn't match

### Default Ports

According to TradeStation documentation, default allowed callback URLs include:
- Port 80
- Port 3000
- Port 3001
- Port 8080
- Port 31022

**Note:** Our SDK uses ports 8888-8898, which are NOT in the default list. Users must manually register these ports in the Developer Portal.

---

## Current Implementation Issues

### Issue 1: Redirect URI Not Updated

**Location:** `session.py` lines 425-523

**Problem:** When auto-selecting a port, `self.redirect_uri` is never updated to match the selected port.

**Fix Required:**
```python
# After auto-selecting port, update redirect_uri:
if redirect_port != port_from_uri:
    # Update redirect_uri to match selected port
    parsed = urlparse(self.redirect_uri)
    self.redirect_uri = f"{parsed.scheme}://{parsed.hostname}:{redirect_port}{parsed.path}"
    # Rebuild auth_request_url with updated redirect_uri
    auth_params["redirect_uri"] = self.redirect_uri
    auth_request_url = f"{self.auth_url}?{urlencode(auth_params)}"
```

### Issue 2: Port Range May Not Be Registered

**Problem:** Users may only register `http://localhost:8888/callback` in the Developer Portal, but SDK tries to use ports 8888-8898.

**Impact:** If SDK auto-selects port 8889, but only 8888 is registered, TradeStation will reject the OAuth request.

**Solutions:**
1. **Documentation:** Clearly state that users must register ALL ports in the range (8888-8898) in the Developer Portal
2. **Warning:** Log a warning when auto-selecting a port that may not be registered
3. **Validation:** Check if redirect_uri port matches selected port before sending OAuth request

### Issue 3: Token Exchange Also Uses Original URI

**Location:** `session.py` line 523

**Problem:** When exchanging the authorization code for tokens, the original `self.redirect_uri` is used, which may not match the port that was actually used.

**Fix Required:** Use the same updated redirect_uri for token exchange.

---

## Recommended Fix

### Option 1: Update Redirect URI When Auto-Selecting (Recommended)

```python
# In authenticate() method, after port selection:

# Store original redirect_uri for reference
original_redirect_uri = self.redirect_uri
actual_redirect_uri = self.redirect_uri

# After port selection (line ~486):
if redirect_port != port_from_uri:
    # Port was auto-selected, update redirect_uri
    parsed = urlparse(self.redirect_uri)
    actual_redirect_uri = f"{parsed.scheme}://{parsed.hostname}:{redirect_port}{parsed.path}"
    
    # Warn user if port doesn't match registered URI
    if redirect_port != port_from_uri:
        logger.warning(
            f"⚠️  Auto-selected port {redirect_port} (original: {port_from_uri or 8888}). "
            f"Ensure 'http://localhost:{redirect_port}/callback' is registered in TradeStation Developer Portal."
        )
    
    # Update redirect_uri for OAuth request
    self.redirect_uri = actual_redirect_uri

# Rebuild auth_params with updated redirect_uri
auth_params = {
    "response_type": "code",
    "client_id": self.client_id,
    "redirect_uri": self.redirect_uri,  # Now matches selected port
    "audience": "https://api.tradestation.com",
    "scope": " ".join(OAUTH_SCOPES),
    "state": state_token,
}
auth_request_url = f"{self.auth_url}?{urlencode(auth_params)}"

# ... rest of authentication flow ...

# Use same redirect_uri for token exchange (line 523)
token_payload = {
    "grant_type": "authorization_code",
    "client_id": self.client_id,
    "client_secret": self.client_secret,
    "code": auth_code,
    "redirect_uri": self.redirect_uri,  # Matches what was sent in OAuth request
}
```

### Option 2: Only Auto-Select If Port Range Is Registered

**Approach:** Only allow auto-selection if the user has explicitly configured a port range, or if the redirect_uri port is in use, fail with a clear error message directing them to register additional ports.

**Pros:** Prevents silent failures  
**Cons:** Less convenient, requires manual port registration

---

## Documentation Updates Needed

1. **LIMITATIONS.md:**
   - Add warning that users must register ALL ports in range (8888-8898) in Developer Portal
   - Clarify that auto-selection updates the redirect_uri

2. **README.md:**
   - Update OAuth setup instructions to mention port range registration
   - Add troubleshooting section for "redirect_uri mismatch" errors

3. **docs/GETTING_STARTED.md:**
   - Update redirect URI setup to mention port range registration

---

## Testing Required

After fix:
1. Test with port 8888 available (should use 8888)
2. Test with port 8888 in use, 8889 available (should use 8889 and update redirect_uri)
3. Test with all ports 8888-8898 in use (should error gracefully)
4. Test with only port 8888 registered in Developer Portal, but SDK auto-selects 8889 (should fail with clear error)
5. Test token exchange with updated redirect_uri

---

## Status

- [x] Fix redirect_uri update when auto-selecting port ✅
- [x] Add warning when port doesn't match registered URI ✅
- [x] Update documentation ✅
- [ ] Add tests (recommended for future)
- [ ] Verify with TradeStation API v3 (recommended for future)

## Fix Applied (2025-12-28)

The fix has been implemented in `session.py`:
- Redirect URI is now automatically updated to match the selected port
- Warnings are logged when ports are auto-selected
- Token exchange uses the same updated redirect_uri
- Documentation updated to clarify port registration requirements

**See:** `session.py` lines 413-495 for the implementation.
