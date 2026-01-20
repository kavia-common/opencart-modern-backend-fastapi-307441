# ⚠️ PLATFORM ACTION REQUIRED - Nginx Configuration

**Issue**: Backend at port 3003 not accessible via external proxy  
**Cause**: Nginx not configured to forward requests to backend  
**Action**: Add nginx proxy configuration  

---

## Quick Fix (Copy-Paste Ready)

Add this to nginx configuration for port 3003:

```nginx
server {
    listen 3003 ssl http2;
    server_name vscode-internal-34084-beta.beta01.cloud.kavia.ai;

    # SSL config (use existing Kavia platform certs)
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Proxy to FastAPI backend
    location / {
        proxy_pass http://127.0.0.1:3003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        proxy_http_version 1.1;
    }
}
```

## Or Minimal (If server block exists)

If there's already a server block for this port, just add:

```nginx
location / {
    proxy_pass http://127.0.0.1:3003;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Apply Configuration

```bash
# Test configuration
nginx -t

# Reload nginx
systemctl reload nginx
# or
nginx -s reload
```

## Verify Fix

```bash
# Should return: {"ping":"pong"}
curl -k https://vscode-internal-34084-beta.beta01.cloud.kavia.ai:3003/ping

# Should show Swagger UI
curl -k https://vscode-internal-34084-beta.beta01.cloud.kavia.ai:3003/docs
```

Or run comprehensive test:

```bash
cd /path/to/opencart-modern-backend-fastapi-307441
./diagnose_proxy.sh
```

---

## Current Status

✅ Backend running on localhost:3003  
✅ All endpoints responding locally  
✅ Backend configured for proxy  
❌ **Nginx not forwarding to backend**  

## What We've Already Done

- Verified backend is running correctly
- Tested all endpoints locally (all working)
- Confirmed proxy headers support enabled
- Created diagnostic tools
- Documented exact configuration needed

## What Platform Team Needs to Do

1. Add nginx configuration (see above)
2. Reload nginx
3. Verify external access works

---

**Urgency**: Medium  
**Impact**: Backend API documentation and external access blocked  
**Complexity**: Low (standard nginx proxy config)  
**ETA**: ~5 minutes to implement and verify  

For detailed troubleshooting: See `PROXY_CONFIGURATION_GUIDE.md`
