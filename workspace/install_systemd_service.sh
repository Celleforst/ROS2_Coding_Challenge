#!/bin/bash
# Post-build script to install systemd service
# Usage: sudo ./install_systemd_service.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/workspace/install/diffdrive_2_acker"
SERVICE_FILE="$INSTALL_DIR/lib/systemd/system/diffdrive_2_acker.service"

if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run as root"
    echo "Usage: sudo $0"
    exit 1
fi

if [ ! -f "$SERVICE_FILE" ]; then
    echo "ERROR: Service file not found: $SERVICE_FILE"
    echo "Make sure to build the package first:"
    echo "  colcon build --packages-select diffdrive_2_acker"
    exit 1
fi

echo "Installing diffdrive_2_acker systemd service..."

# Copy service file
cp "$SERVICE_FILE" /etc/systemd/system/diffdrive_2_acker.service
echo "Copied service file"

# Reload systemd
systemctl daemon-reload
echo "Reloaded systemd"

# Enable the service
systemctl enable diffdrive_2_acker.service
echo "Enabled service"

# Start the service
systemctl start diffdrive_2_acker.service
echo "Started service"

echo ""
echo "SUCCESS: Systemd service installed and running!"
echo ""