#!/bin/bash

# Script to deploy the Human Designs Next.js frontend as a systemd service.
# Supports 'test' and 'production' modes.

SERVICE_NAME="human-designs-frontend.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
FRONTEND_DIR="/home/a112/Documents/code/personal/human-designs" # Project root
USER=$(whoami)
GROUP=$(id -gn)

# Default values
MODE=""
PORT="" # Will be determined based on mode

# Function to display script usage
usage() {
    echo "Usage: $0 --mode <test|production> [--port <port_number>]"
    echo "  --mode      Deployment mode: 'test' or 'production'."
    echo "  --port      (Optional) Custom port. Defaults to 3000 for test, 3000 for production (assuming Next.js default)."
    exit 1
}

# Function to find a free port (similar to backend script)
find_free_port() {
    local start_port=3000
    local end_port=3100
    local free_port=""

    for p in $(seq "$start_port" "$end_port"); do
        if ! sudo netstat -tuln | grep -q ":$p\b"; then
            free_port="$p"
            break
        fi
    done

    if [ -z "$free_port" ]; then
        echo "Error: No free ports found in range $start_port-$end_port."
        exit 1
    fi
    echo "$free_port"
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --mode)
            MODE="$2"
            shift
            ;;
        --port)
            PORT="$2"
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            usage
            ;;
    esac
    shift
done

# Validate mode
if [ -z "$MODE" ]; then
    echo "Error: --mode is required."
    usage
fi

if [[ "$MODE" != "test" && "$MODE" != "production" ]]; then
    echo "Error: --mode must be 'test' or 'production'."
    usage
fi

# Determine port and command based on mode
NPM_COMMAND=""
if [ "$MODE" == "production" ]; then
    if [ -z "$PORT" ]; then
        PORT=3000 # Default production port
    fi
    NPM_COMMAND="npm run start"
    echo "Building frontend for production..."
    cd "$FRONTEND_DIR" || { echo "Error: Frontend directory not found."; exit 1; }
    npm run build || { echo "Error: Frontend build failed."; exit 1; }
    cd - > /dev/null # Go back to original directory
elif [ "$MODE" == "test" ]; then
    if [ -z "$PORT" ]; then
        echo "Finding a free port for test mode..."
        PORT=$(find_free_port)
        echo "Found free port: $PORT"
    fi
    NPM_COMMAND="npm run dev"
fi

if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid port number: $PORT"
    exit 1
fi

echo "Deploying Next.js frontend service in $MODE mode on port $PORT..."

# Stop and disable existing service if it exists
if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    echo "Stopping existing $SERVICE_NAME..."
    sudo systemctl stop "$SERVICE_NAME"
fi
if sudo systemctl is-enabled --quiet "$SERVICE_NAME"; then
    echo "Disabling existing $SERVICE_NAME..."
    sudo systemctl disable "$SERVICE_NAME"
fi
if [ -f "$SERVICE_FILE" ]; then
    echo "Removing existing service file $SERVICE_FILE..."
    sudo rm "$SERVICE_FILE"
fi

# Create the systemd service file
cat <<EOF | sudo tee "$SERVICE_FILE" > /dev/null
[Unit]
Description=Human Designs Next.js Frontend Application (${MODE} mode)
After=network.target

[Service]
User=${USER}
Group=${GROUP}
WorkingDirectory=${FRONTEND_DIR}
ExecStart=/bin/bash -c "PORT=${PORT} ${NPM_COMMAND}"
Restart=on-failure
# Ensure Node.js and npm are in the PATH
Environment="PATH=/usr/bin:/bin:/usr/local/bin:/usr/sbin:/sbin:/usr/local/sbin:${FRONTEND_DIR}/node_modules/.bin"

[Install]
WantedBy=multi-user.target
EOF

if [ $? -ne 0 ]; then
    echo "Error: Failed to create systemd service file."
    exit 1
fi

echo "Systemd service file created at $SERVICE_FILE"

# Reload systemd daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
if [ $? -ne 0 ]; then
    echo "Error: Failed to reload systemd daemon."
    exit 1
fi

# Enable the service
echo "Enabling $SERVICE_NAME..."
sudo systemctl enable "$SERVICE_NAME"
if [ $? -ne 0 ]; then
    echo "Error: Failed to enable service."
    exit 1
fi

# Start the service
echo "Starting $SERVICE_NAME..."
sudo systemctl start "$SERVICE_NAME"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start service."
    exit 1
fi

echo "Service $SERVICE_NAME deployed and started successfully."
echo "You can check its status with: sudo systemctl status $SERVICE_NAME"
echo "You can stop it with: sudo systemctl stop $SERVICE_NAME"
echo "You can restart it with: sudo systemctl restart $SERVICE_NAME"
