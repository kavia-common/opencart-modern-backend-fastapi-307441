#!/bin/bash
# Quick endpoint test script

echo "Testing Local Backend Endpoints..."
echo ""

curl -s http://localhost:3003/ping && echo ""
curl -s http://localhost:3003/health && echo ""
curl -s http://localhost:3003/ | python3 -m json.tool | head -20

echo ""
echo "Testing External Proxy..."
echo ""

curl -k -s https://vscode-internal-34084-beta.beta01.cloud.kavia.ai:3003/ping && echo ""
curl -k -s https://vscode-internal-34084-beta.beta01.cloud.kavia.ai:3003/health && echo ""
