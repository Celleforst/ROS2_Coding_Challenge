#!/bin/bash
set -e

# Create XDG runtime directory (needed for Wayland/GUI apps)
# This needs to be created at runtime since /run is a tmpfs
USER_UID=${USER_UID:-1000}
USER_GID=${USER_GID:-1000}
mkdir -p /run/user/$USER_UID
chown $USER_UID:$USER_GID /run/user/$USER_UID
chmod 700 /run/user/$USER_UID

# Source ROS 2 environment
source /opt/ros/humble/setup.bash

# Source workspace if it has been built
if [ -f "/workspace/install/setup.bash" ]; then
    source /workspace/install/setup.bash
fi

# Keep container running
exec "$@"

