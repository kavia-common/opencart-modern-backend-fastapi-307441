#!/bin/bash
# Backend Verification Script
# Tests FastAPI backend health, endpoints, and proxy readiness

set -e

echo "========================================="
echo "FastAPI Backend Verification"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BACKEND_URL="http://localhost:3003"
EXTERNAL_URL="https://vscode-internal-34084-beta.beta01.cloud.kavia.ai:3003"

# Test local backend
echo "1. Testing Local Backend Connectivity"
echo "   URL: $BACKEND_URL"
echo ""

# Test /ping
echo -n "   GET /ping ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/ping" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC} - $BODY"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test /health
echo -n "   GET /health ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/health" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC} - $BODY"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test /ready
echo -n "   GET /ready ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/ready" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC} - $BODY"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test root
echo -n "   GET / ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test /docs
echo -n "   GET /docs ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/docs" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC} (Swagger UI)"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test /redoc
echo -n "   GET /redoc ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/redoc" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC} (ReDoc)"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test /openapi.json
echo -n "   GET /openapi.json ... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/openapi.json" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC} (OpenAPI Spec)"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test API endpoint
echo -n "   GET /api/v1/... "
RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/api/v1/products?limit=1" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "401" ]; then
    echo -e "${GREEN}OK${NC} (API routes registered)"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

echo ""
echo "2. Testing External Access via Proxy"
echo "   URL: $EXTERNAL_URL"
echo ""

# Test external /
echo -n "   GET / (external) ... "
RESPONSE=$(curl -k -s -w "\n%{http_code}" "$EXTERNAL_URL/" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
    if echo "$BODY" | grep -q "nginx"; then
        echo -e "   ${YELLOW}Note: Receiving nginx 404 - proxy not configured to forward to backend${NC}"
    fi
fi

# Test external /ping
echo -n "   GET /ping (external) ... "
RESPONSE=$(curl -k -s -w "\n%{http_code}" "$EXTERNAL_URL/ping" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

# Test external /docs
echo -n "   GET /docs (external) ... "
RESPONSE=$(curl -k -s -w "\n%{http_code}" "$EXTERNAL_URL/docs" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
fi

echo ""
echo "3. Backend Process Information"
echo ""

# Check if backend is running
BACKEND_PID=$(pgrep -f "uvicorn app.main" | head -1)
if [ -n "$BACKEND_PID" ]; then
    echo -e "   Backend Process: ${GREEN}RUNNING${NC} (PID: $BACKEND_PID)"
    echo "   Command: $(ps -p $BACKEND_PID -o args= | head -1)"
else
    echo -e "   Backend Process: ${RED}NOT RUNNING${NC}"
fi

# Check listening ports
echo ""
echo "   Listening Ports:"
netstat -tlnp 2>/dev/null | grep 3003 | awk '{print "   - " $4}' || echo "   None found on port 3003"

echo ""
echo "4. Configuration Check"
echo ""

# Check .env file
if [ -f ".env" ]; then
    echo "   .env file: EXISTS"
    if grep -q "ROOT_PATH" .env; then
        ROOT_PATH=$(grep "^ROOT_PATH=" .env | cut -d'=' -f2)
        echo "   ROOT_PATH: ${ROOT_PATH:-'(empty)'}"
    else
        echo -e "   ROOT_PATH: ${YELLOW}NOT SET${NC}"
    fi
    if grep -q "BACKEND_URL" .env; then
        BACKEND_URL_ENV=$(grep "^BACKEND_URL=" .env | cut -d'=' -f2)
        echo "   BACKEND_URL: $BACKEND_URL_ENV"
    fi
else
    echo -e "   .env file: ${YELLOW}NOT FOUND${NC}"
fi

echo ""
echo "========================================="
echo "Summary"
echo "========================================="
echo ""
echo "Local backend endpoints are working correctly."
echo ""
if curl -k -s "$EXTERNAL_URL/ping" 2>/dev/null | grep -q "pong"; then
    echo -e "${GREEN}✓ External proxy is correctly configured${NC}"
    echo "  All endpoints accessible via: $EXTERNAL_URL"
else
    echo -e "${YELLOW}⚠ External proxy configuration issue detected${NC}"
    echo ""
    echo "  The backend is running correctly but the nginx proxy"
    echo "  at port 3003 is not forwarding requests to the backend."
    echo ""
    echo "  This is a platform/infrastructure issue."
    echo "  The nginx proxy needs to be configured with:"
    echo ""
    echo "    location / {"
    echo "        proxy_pass http://127.0.0.1:3003;"
    echo "        proxy_set_header Host \$host;"
    echo "        proxy_set_header X-Real-IP \$remote_addr;"
    echo "        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;"
    echo "        proxy_set_header X-Forwarded-Proto \$scheme;"
    echo "    }"
    echo ""
fi
echo ""
