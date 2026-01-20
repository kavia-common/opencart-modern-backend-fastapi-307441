# FastAPI Backend Deployment Guide

## Overview

This FastAPI backend serves the OpenCart Modern API on port 3003. It includes automatic API documentation via Swagger UI and ReDoc.

## Quick Start

### Development Mode
```bash
./start.sh
```

### Production Mode
```bash
./start-prod.sh
```

## Accessing the API

### Local Access
- **API Root**: http://localhost:3003/
- **Swagger UI**: http://localhost:3003/docs
- **ReDoc**: http://localhost:3003/redoc
- **OpenAPI Spec**: http://localhost:3003/openapi.json
- **Health Check**: http://localhost:3003/health
- **Ping**: http://localhost:3003/ping

### Through Reverse Proxy
If deployed behind nginx or another reverse proxy, ensure the proxy is configured to forward requests to the backend.

## Configuration

### Environment Variables

The following environment variables can be set in `.env`:

#### Server Configuration
- `HOST` - Bind address (default: 0.0.0.0)
- `PORT` - Port number (default: 3003)
- `WORKERS` - Number of worker processes (default: 1 for dev, 4 for prod)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

#### Proxy Configuration
- `ROOT_PATH` - If the app is mounted at a subpath (e.g., "/api")
- `FORWARDED_ALLOW_IPS` - IPs to trust for X-Forwarded-* headers (default: *)

#### CORS Configuration
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins

## Reverse Proxy Setup

### Nginx Configuration Example

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL configuration
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
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Key Points for Proxy Configuration

1. **Proxy Headers**: The FastAPI app is configured with `--proxy-headers` to trust X-Forwarded-* headers
2. **Host Header**: Must be forwarded correctly for CORS to work
3. **SSL/TLS**: If using HTTPS, ensure X-Forwarded-Proto is set to "https"

## Troubleshooting

### 404 Not Found from Nginx

If you see a 404 error from nginx when accessing the API:

1. **Verify Backend is Running**:
   ```bash
   curl http://localhost:3003/ping
   ```
   Should return: `{"ping":"pong"}`

2. **Check Nginx Configuration**:
   - Ensure `proxy_pass` points to the correct backend address
   - Verify nginx can reach the backend (check firewall rules)
   - Test nginx config: `nginx -t`

3. **Check Nginx Logs**:
   ```bash
   tail -f /var/log/nginx/error.log
   tail -f /var/log/nginx/access.log
   ```

4. **Verify Proxy Headers**:
   The app logs all incoming requests with headers. Check the FastAPI logs to see if requests are reaching the backend.

### Check Application Logs

The application logs all incoming requests including headers, which helps diagnose proxy issues:

```bash
# If running in foreground, check console output
# If running as a service, check systemd logs:
journalctl -u your-fastapi-service -f
```

### Test Connectivity

```bash
# Test basic connectivity
curl http://localhost:3003/ping

# Test API root
curl http://localhost:3003/

# Test Swagger docs
curl http://localhost:3003/docs

# Test with headers (simulate proxy)
curl -H "X-Forwarded-For: 1.2.3.4" \
     -H "X-Forwarded-Proto: https" \
     http://localhost:3003/
```

## Health Checks

### Endpoints

1. **`/ping`** - Simple connectivity test, returns immediately
2. **`/health`** - Basic health check, confirms app is running
3. **`/ready`** - Readiness check, verifies database connectivity

### Usage in Load Balancers

```yaml
# Example for Kubernetes
livenessProbe:
  httpGet:
    path: /health
    port: 3003
  initialDelaySeconds: 5
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 3003
  initialDelaySeconds: 10
  periodSeconds: 5
```

## Common Issues

### Issue: Cannot Access Swagger UI

**Solution**: 
1. Verify the app is running: `curl http://localhost:3003/ping`
2. Check `DOCS_URL` in config (should be "/docs")
3. Access directly: `http://localhost:3003/docs`

### Issue: CORS Errors

**Solution**:
1. Add your frontend URL to `ALLOWED_ORIGINS` in `.env`
2. Ensure proxy forwards `Origin` header correctly
3. Check FastAPI logs for CORS-related messages

### Issue: 502 Bad Gateway

**Solution**:
1. Verify backend is running and listening on correct port
2. Check firewall rules between proxy and backend
3. Verify proxy configuration points to correct address:port

## Production Deployment Checklist

- [ ] Set strong `SECRET_KEY` in `.env`
- [ ] Configure `ALLOWED_ORIGINS` with actual frontend URLs
- [ ] Set `DEBUG=False` for production
- [ ] Configure `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Set appropriate `WORKERS` count (typically 2-4 per CPU core)
- [ ] Set up SSL/TLS termination at proxy level
- [ ] Configure proper proxy headers in nginx/load balancer
- [ ] Set up monitoring and log aggregation
- [ ] Configure database backups
- [ ] Test health check endpoints
- [ ] Verify API documentation is accessible

## Support

For issues related to:
- **Application code**: Check application logs
- **Deployment/proxy**: Check this guide and nginx logs
- **Database**: Check `DATABASE_URL` configuration and database logs
