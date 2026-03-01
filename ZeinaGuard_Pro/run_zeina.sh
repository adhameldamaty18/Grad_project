#!/bin/bash
# ZeinaGuard Pro | Production Deployment Script
# Description: Automated integrity check and Docker environment orchestration.

echo "------------------------------------------------"
echo "🛡️  ZeinaGuard Pro | Enterprise WIPS"
echo "------------------------------------------------"

# 1. System Integrity Audit
# Define the core components required for a successful boot
REQUIRED_FILES=(
    "app.py" 
    "config.py" 
    "requirements.txt" 
    "Dockerfile" 
    "docker-compose.yml"
    "database/db_manager.py"
    "api/routes.py"
    "engine/threat_analyzer.py"
    "templates/dashboard.html"
)

MISSING_COUNT=0

echo "[*] Auditing system integrity..."

# Iterate through the manifest to verify file presence
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo " [!] CRITICAL ERROR: Missing component -> $file"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    fi
done

# Ensure the data persistence layer exists for the SQLite database
if [ ! -d "data" ]; then
    echo "[+] Initializing persistence layer: 'data/' directory..."
    mkdir -p data
fi

# 2. Safety Gate: Halt deployment if the system is incomplete
if [ $MISSING_COUNT -gt 0 ]; then
    echo "------------------------------------------------"
    echo " ERROR: Integrity check failed. $MISSING_COUNT file(s) missing."
    echo " Please verify the project structure before proceeding."
    echo "------------------------------------------------"
    exit 1
fi

echo "[+] Integrity verified. System state: HEALTHY."

# 3. Docker Container Orchestration
# Rebuild images if code changes are detected and start in detached mode
echo "[*] Orchestrating Docker containers (Build & Up)..."
sudo docker-compose up --build -d

echo "------------------------------------------------"
echo "🚀 DEPLOYMENT COMPLETED SUCCESSFULLY"
echo "🌍 Access Dashboard: http://localhost:5000"
echo "------------------------------------------------"

# 4. Telemetry Monitoring
# Attach to the log stream to monitor real-time threat detection
echo "[*] Attaching to service logs (Press Ctrl+C to detach):"
sudo docker-compose logs -f