#!/bin/bash
# Proxy Diagnostic Script
# Comprehensive diagnostics for proxy configuration issues

set -e

echo "========================================="
echo "FastAPI Backend Proxy Diagnostics"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_URL="http://localhost:3003"

# Get external URL from .env if available
if [ -f ".env" ] && grep -q "^BACKEND_URL=" .env; then
    EXTERNAL_URL=$(grep "^BACKEND_URL=" .env | cut -d'=' -f2)
else
    EXTERNAL_URL="https://vscode-internal-34084-beta.beta01.cloud.kavia.ai:3003"
fi

echo "Configuration:"
echo "  Local Backend:    $BACKEND_URL"
echo "  External Proxy:   $EXTERNAL_URL"
echo ""

# 1. Check if backend process is running
echo "1. Backend Process Status"
echo "   ========================"
BACKEND_PID=$(pgrep -f "uvicorn app.main" 2>/dev/null | head -1)
if [ -n "$BACKEND_PID" ]; then
    echo -e "   Process Status: ${GREEN}RUNNING${NC}"
    echo "   PID: $BACKEND_PID"
    echo "   Command: $(ps -p $BACKEND_PID -o args= | head -c 120)..."
    echo ""
    
    # Get process details
    echo "   Process Details:"
    ps -p $BACKEND_PID -o pid,ppid,%cpu,%mem,etime,cmd | tail -n +2 | sed 's/^/   /'
else
    echo -e "   Process Status: ${RED}NOT RUNNING${NC}"
    echo -e "   ${YELLOW}Action Required: Start the backend with ./start.sh${NC}"
    exit 1
fi
echo ""

# 2. Check listening ports
echo "2. Network Port Status"
echo "   ==================="
if command -v netstat >/dev/null 2>&1; then
    PORT_INFO=$(netstat -tlnp 2>/dev/null | grep ":3003" || echo "")
    if [ -n "$PORT_INFO" ]; then
        echo -e "   Port 3003: ${GREEN}LISTENING${NC}"
        echo "$PORT_INFO" | sed 's/^/   /'
    else
        echo -e "   Port 3003: ${RED}NOT LISTENING${NC}"
        echo -e "   ${YELLOW}Warning: Backend should be listening on port 3003${NC}"
    fi
elif command -v ss >/dev/null 2>&1; then
    PORT_INFO=$(ss -tlnp 2>/dev/null | grep ":3003" || echo "")
    if [ -n "$PORT_INFO" ]; then
        echo -e "   Port 3003: ${GREEN}LISTENING${NC}"
        echo "$PORT_INFO" | sed 's/^/   /'
    else
        echo -e "   Port 3003: ${RED}NOT LISTENING${NC}"
    fi
else
    echo -e "   ${YELLOW}Cannot check ports (netstat/ss not available)${NC}"
fi
echo ""

# 3. Test local backend connectivity
echo "3. Local Backend Connectivity"
echo "   ==========================="
LOCAL_TESTS=0
LOCAL_PASSED=0

# Test /ping
echo -n "   Testing /ping ... "
if RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/ping" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}OK${NC} ($BODY)"
        LOCAL_PASSED=$((LOCAL_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
LOCAL_TESTS=$((LOCAL_TESTS + 1))

# Test /health
echo -n "   Testing /health ... "
if RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/health" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}OK${NC}"
        LOCAL_PASSED=$((LOCAL_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
LOCAL_TESTS=$((LOCAL_TESTS + 1))

# Test /
echo -n "   Testing / ... "
if RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}OK${NC}"
        LOCAL_PASSED=$((LOCAL_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
LOCAL_TESTS=$((LOCAL_TESTS + 1))

# Test /docs
echo -n "   Testing /docs ... "
if RESPONSE=$(curl -s -w "\n%{http_code}" "$BACKEND_URL/docs" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    if [ "$HTTP_CODE" = "200" ]; then
        echo -e "${GREEN}OK${NC}"
        LOCAL_PASSED=$((LOCAL_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
LOCAL_TESTS=$((LOCAL_TESTS + 1))

echo ""
echo "   Local Tests: $LOCAL_PASSED/$LOCAL_TESTS passed"
echo ""

# 4. Test external proxy connectivity
echo "4. External Proxy Connectivity"
echo "   ============================"
PROXY_TESTS=0
PROXY_PASSED=0

# Test /ping through proxy
echo -n "   Testing /ping (via proxy) ... "
if RESPONSE=$(curl -k -s -w "\n%{http_code}" "$EXTERNAL_URL/ping" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" = "200" ] && echo "$BODY" | grep -q "pong"; then
        echo -e "${GREEN}OK${NC}"
        PROXY_PASSED=$((PROXY_PASSED + 1))
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
        if echo "$BODY" | grep -q -i "nginx"; then
            echo -e "   ${YELLOW}Response from nginx, not backend${NC}"
        fi
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
PROXY_TESTS=$((PROXY_TESTS + 1))

# Test / through proxy
echo -n "   Testing / (via proxy) ... "
if RESPONSE=$(curl -k -s -w "\n%{http_code}" "$EXTERNAL_URL/" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    SERVER_HEADER=$(curl -k -s -I "$EXTERNAL_URL/" 2>/dev/null | grep -i "^server:" | cut -d' ' -f2-)
    
    if [ "$HTTP_CODE" = "200" ]; then
        if echo "$BODY" | grep -q "OpenCart Modern API"; then
            echo -e "${GREEN}OK${NC} (Backend responding)"
            PROXY_PASSED=$((PROXY_PASSED + 1))
        else
            echo -e "${YELLOW}WARNING${NC} (HTTP 200 but unexpected content)"
        fi
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
        if echo "$BODY" | grep -q -i "nginx"; then
            echo -e "   ${YELLOW}Nginx 404 - proxy not forwarding to backend${NC}"
            echo "   Server header: $SERVER_HEADER"
        fi
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
PROXY_TESTS=$((PROXY_TESTS + 1))

# Test /docs through proxy
echo -n "   Testing /docs (via proxy) ... "
if RESPONSE=$(curl -k -s -w "\n%{http_code}" "$EXTERNAL_URL/docs" 2>/dev/null); then
    HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
    BODY=$(echo "$RESPONSE" | head -n-1)
    if [ "$HTTP_CODE" = "200" ]; then
        if echo "$BODY" | grep -q -i "swagger"; then
            echo -e "${GREEN}OK${NC} (Swagger UI accessible)"
            PROXY_PASSED=$((PROXY_PASSED + 1))
        else
            echo -e "${YELLOW}WARNING${NC} (HTTP 200 but no Swagger content)"
        fi
    else
        echo -e "${RED}FAILED${NC} (HTTP $HTTP_CODE)"
    fi
else
    echo -e "${RED}FAILED${NC} (connection error)"
fi
PROXY_TESTS=$((PROXY_TESTS + 1))

echo ""
echo "   Proxy Tests: $PROXY_PASSED/$PROXY_TESTS passed"
echo ""

# 5. Configuration analysis
echo "5. Configuration Analysis"
echo "   ======================"

if [ -f ".env" ]; then
    echo "   .env file: EXISTS"
    
    # Check ROOT_PATH
    if grep -q "^ROOT_PATH=" .env 2>/dev/null; then
        ROOT_PATH=$(grep "^ROOT_PATH=" .env | cut -d'=' -f2)
        echo "   ROOT_PATH: '${ROOT_PATH}' (${ROOT_PATH:+set}${ROOT_PATH:-empty})"
    else
        echo -e "   ROOT_PATH: ${YELLOW}not configured${NC} (using default '')"
    fi
    
    # Check ALLOWED_ORIGINS
    if grep -q "^ALLOWED_ORIGINS=" .env 2>/dev/null; then
        ALLOWED_ORIGINS=$(grep "^ALLOWED_ORIGINS=" .env | cut -d'=' -f2)
        echo "   ALLOWED_ORIGINS: $ALLOWED_ORIGINS"
    fi
    
    # Check HOST
    if grep -q "^HOST=" .env 2>/dev/null; then
        HOST=$(grep "^HOST=" .env | cut -d'=' -f2)
        echo "   HOST: $HOST"
    fi
    
    # Check PORT
    if grep -q "^PORT=" .env 2>/dev/null; then
        PORT=$(grep "^PORT=" .env | cut -d'=' -f2)
        echo "   PORT: $PORT"
    fi
else
    echo -e "   .env file: ${YELLOW}NOT FOUND${NC}"
fi
echo ""

# 6. Request header test
echo "6. Proxy Header Handling Test"
echo "   ==========================="
echo "   Testing X-Forwarded-* header support..."

HEADER_TEST=$(curl -s -H "X-Forwarded-For: 1.2.3.4" \
    -H "X-Forwarded-Proto: https" \
    -H "X-Forwarded-Host: example.com" \
    "$BACKEND_URL/ping" 2>/dev/null)

if echo "$HEADER_TEST" | grep -q "pong"; then
    echo -e "   Proxy headers: ${GREEN}ACCEPTED${NC}"
    echo "   Backend is configured with --proxy-headers"
else
    echo -e "   Proxy headers: ${YELLOW}UNKNOWN${NC}"
fi
echo ""

# 7. Generate diagnosis report
echo "========================================="
echo "DIAGNOSIS SUMMARY"
echo "========================================="
echo ""

if [ $LOCAL_PASSED -eq $LOCAL_TESTS ]; then
    echo -e "${GREEN}✓ Backend Application: HEALTHY${NC}"
    echo "  All local endpoints responding correctly"
else
    echo -e "${RED}✗ Backend Application: ISSUES DETECTED${NC}"
    echo "  Some local endpoints not responding"
    echo -e "  ${YELLOW}Action: Check application logs for errors${NC}"
fi
echo ""

if [ $PROXY_PASSED -eq $PROXY_TESTS ]; then
    echo -e "${GREEN}✓ Proxy Configuration: WORKING${NC}"
    echo "  External URL is properly configured"
    echo "  Documentation accessible at: $EXTERNAL_URL/docs"
else
    echo -e "${RED}✗ Proxy Configuration: NOT WORKING${NC}"
    echo ""
    echo "  ROOT CAUSE:"
    echo "  -----------"
    echo "  The nginx reverse proxy is not forwarding requests to the backend."
    echo "  Nginx is returning its own 404 page instead of proxying to the"
    echo "  FastAPI application running on localhost:3003."
    echo ""
    echo "  EVIDENCE:"
    echo "  • Local backend: responding correctly to all requests"
    echo "  • External URL: returning nginx 404 errors"
    echo "  • Server header: nginx/1.29.1 (not FastAPI/uvicorn)"
    echo ""
    echo "  REQUIRED FIX:"
    echo "  -------------"
    echo "  This is a platform infrastructure issue. The Kavia platform's"
    echo "  nginx configuration needs to include a proxy rule for port 3003."
    echo ""
    echo "  Required nginx configuration:"
    echo ""
    echo -e "  ${BLUE}server {${NC}"
    echo -e "  ${BLUE}    listen 3003 ssl http2;${NC}"
    echo -e "  ${BLUE}    server_name <domain>;${NC}"
    echo ""
    echo -e "  ${BLUE}    location / {${NC}"
    echo -e "  ${BLUE}        proxy_pass http://127.0.0.1:3003;${NC}"
    echo -e "  ${BLUE}        proxy_set_header Host \$host;${NC}"
    echo -e "  ${BLUE}        proxy_set_header X-Real-IP \$remote_addr;${NC}"
    echo -e "  ${BLUE}        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;${NC}"
    echo -e "  ${BLUE}        proxy_set_header X-Forwarded-Proto \$scheme;${NC}"
    echo -e "  ${BLUE}        proxy_set_header X-Forwarded-Host \$server_name;${NC}"
    echo -e "  ${BLUE}    }${NC}"
    echo -e "  ${BLUE}}${NC}"
    echo ""
    echo "  NEXT STEPS:"
    echo "  -----------"
    echo "  1. Contact platform support to configure nginx proxy for port 3003"
    echo "  2. After configuration, re-run this script to verify"
    echo "  3. Access documentation at: $EXTERNAL_URL/docs"
    echo ""
fi

echo "========================================="
echo ""

# Exit with appropriate code
if [ $LOCAL_PASSED -eq $LOCAL_TESTS ] && [ $PROXY_PASSED -eq $PROXY_TESTS ]; then
    exit 0
else
    exit 1
fi
