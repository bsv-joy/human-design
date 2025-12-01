#!/bin/bash

# Script to deploy a test environment for both frontend and backend
# by deploying them as systemd services.

FRONTEND_DEPLOY_SCRIPT="./deploy_frontend_service.sh"
BACKEND_DEPLOY_SCRIPT="deploy_fastapi_service.sh"


# Variables to store dynamically assigned ports
BACKEND_ASSIGNED_PORT=""
FRONTEND_ASSIGNED_PORT=""

echo "--- Deploying Human Designs Backend Service (Test Mode) ---"
# Call the backend deployment script with test mode. It will find a free port.
# Capture output to find the assigned port
BACKEND_OUTPUT=$(scripts/"$BACKEND_DEPLOY_SCRIPT" --mode test 2>&1)
BACKEND_EXIT_CODE=$?
echo "$BACKEND_OUTPUT" # Print the full output for debugging/user info

if [ $BACKEND_EXIT_CODE -ne 0 ]; then
    echo "Error: Backend deployment failed. Aborting."
    exit 1
fi

# Extract the assigned port from the backend script's output
BACKEND_ASSIGNED_PORT=$(echo "$BACKEND_OUTPUT" | grep -oP 'Found free port: \K[0-9]+' | head -n 1)
if [ -z "$BACKEND_ASSIGNED_PORT" ]; then
    echo "Error: Could not determine backend assigned port. Aborting."
    exit 1
fi
echo "Backend deployed on port: $BACKEND_ASSIGNED_PORT"
echo ""

echo "--- Deploying Human Designs Frontend Service (Test Mode) ---"
# Call the frontend deployment script with test mode. It will find a free port.
# Capture output to find the assigned port
FRONTEND_OUTPUT=$(scripts/"$FRONTEND_DEPLOY_SCRIPT" --mode test 2>&1)
FRONTEND_EXIT_CODE=$?
echo "$FRONTEND_OUTPUT" # Print the full output for debugging/user info

if [ $FRONTEND_EXIT_CODE -ne 0 ]; then
    echo "Error: Frontend deployment failed. Aborting."
    exit 1
fi

# Extract the assigned port from the frontend script's output
FRONTEND_ASSIGNED_PORT=$(echo "$FRONTEND_OUTPUT" | grep -oP 'Found free port: \K[0-9]+' | head -n 1)
if [ -z "$FRONTEND_ASSIGNED_PORT" ]; then
    echo "Error: Could not determine frontend assigned port. Aborting."
    exit 1
fi
echo "Frontend deployed on port: $FRONTEND_ASSIGNED_PORT"
echo ""

echo "--- Test Environment Deployment Complete ---"
echo "Frontend accessible at: http://localhost:$FRONTEND_ASSIGNED_PORT"
echo "Backend API accessible at: http://localhost:$BACKEND_ASSIGNED_PORT"

echo ""
echo "To check service status:"
echo "  sudo systemctl status human-designs-frontend.service"
echo "  sudo systemctl status human-designs-fastapi.service"
echo ""
echo "To stop services:"
echo "  sudo systemctl stop human-designs-frontend.service"
echo "  sudo systemctl stop human-designs-fastapi.service"
echo ""
echo "To restart services:"
echo "  sudo systemctl restart human-designs-frontend.service"
echo "  sudo systemctl restart human-designs-fastapi.service"
echo ""
echo "Note: The services are configured with 'Restart=on-failure' and 'Reload' (for backend dev server)."
echo "For frontend 'test' mode, it runs 'npm run dev', which usually handles hot-reloading."

