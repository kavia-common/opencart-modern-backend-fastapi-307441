#!/bin/bash
# Make all shell scripts executable

chmod +x start.sh
chmod +x start-prod.sh
chmod +x verify_backend.sh
chmod +x diagnose_proxy.sh
chmod +x run_tests.sh
chmod +x test_endpoints.sh

echo "All scripts are now executable"
ls -lh *.sh
