#!/bin/bash

# Script to stop the Human Designs test environment systemd services.

FRONTEND_SERVICE_NAME="human-designs-frontend.service"
BACKEND_SERVICE_NAME="human-designs-fastapi.service"

echo "--- Stopping Human Designs Test Environment ---"

echo "Stopping frontend service: $FRONTEND_SERVICE_NAME..."
sudo systemctl stop "$FRONTEND_SERVICE_NAME"
if [ $? -eq 0 ]; then
    echo "$FRONTEND_SERVICE_NAME stopped successfully."
else
    echo "Error: Failed to stop $FRONTEND_SERVICE_NAME. Check its status with 'sudo systemctl status $FRONTEND_SERVICE_NAME'."
fi

echo "Stopping backend service: $BACKEND_SERVICE_NAME..."
sudo systemctl stop "$BACKEND_SERVICE_NAME"
if [ $? -eq 0 ]; then
    echo "$BACKEND_SERVICE_NAME stopped successfully."
else
    echo "Error: Failed to stop $BACKEND_SERVICE_NAME. Check its status with 'sudo systemctl status $BACKEND_SERVICE_NAME'."
fi

echo ""
echo "Disabling frontend service: $FRONTEND_SERVICE_NAME to prevent auto-start on reboot..."
sudo systemctl disable "$FRONTEND_SERVICE_NAME"
if [ $? -eq 0 ]; then
    echo "$FRONTEND_SERVICE_NAME disabled successfully."
else
    echo "Warning: Failed to disable $FRONTEND_SERVICE_NAME."
fi

echo "Disabling backend service: $BACKEND_SERVICE_NAME to prevent auto-start on reboot..."
sudo systemctl disable "$BACKEND_SERVICE_NAME"
if [ $? -eq 0 ]; then
    echo "$BACKEND_SERVICE_NAME disabled successfully."
else
    echo "Warning: Failed to disable $BACKEND_SERVICE_NAME."
fi

echo ""
echo "Human Designs Test Environment services have been stopped and disabled."
