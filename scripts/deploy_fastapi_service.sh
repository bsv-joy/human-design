#!/bin/bash

# Script to deploy the Human Designs FastAPI service as a systemd service.
# Supports 'test' and 'production' modes with custom port mapping for testing.

SERVICE_NAME="human-designs-fastapi.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
BACKEND_DIR="/home/a112/Documents/code/personal/human-designs/backend"
USER=$(whoami)
GROUP=$(id -gn)

# Default values
MODE=""
PORT="" # Will be determined based on mode

# Function to display script usage
usage() {
    echo "Usage: $0 --mode <test|production> [--port <port_number>]"
    echo "  --mode      Deployment mode: 'test' or 'production'."
    echo "  --port      (Optional) Custom port for 'test' mode. If not provided, a free port will be found."
    exit 1
}

# Function to find a free port
find_free_port() {
    local start_port=8000
    local end_port=9000
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

# Determine port based on mode
if [ "$MODE" == "production" ]; then
    if [ -n "$PORT" ]; then
        echo "Warning: --port is ignored in production mode. Using static port 8000."
    fi
    PORT=8000
elif [ "$MODE" == "test" ]; then
    if [ -z "$PORT" ]; then
        echo "Finding a free port for test mode..."
        PORT=$(find_free_port)
        echo "Found free port: $PORT"
    fi
fi

if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid port number: $PORT"
    exit 1
fi

echo "Deploying FastAPI service in $MODE mode on port $PORT..."

# Create the systemd service file
cat <<EOF | sudo tee "$SERVICE_FILE" > /dev/null
[Unit]
Description=Human Designs FastAPI Application (${MODE} mode)
After=network.target

[Service]
User=${USER}
Group=${GROUP}
WorkingDirectory=${BACKEND_DIR}
ExecStart=/bin/bash -c "source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port ${PORT}"
Restart=on-failure
Environment="PATH=${BACKEND_DIR}/.venv/bin:\$PATH"

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