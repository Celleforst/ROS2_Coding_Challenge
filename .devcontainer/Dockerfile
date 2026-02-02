FROM osrf/ros:humble-desktop-full

ARG USERNAME=devuser
ARG USER_UID=1000
ARG USER_GID=1000

# Install needed deps (include systemd so we can run system services)
RUN apt-get update && apt-get install -y --no-install-recommends \
    systemd systemd-sysv dbus \
    vim sudo tmux python3-pip \
    ros-${ROS_DISTRO}-rosbag2-storage-mcap ros-${ROS_DISTRO}-foxglove-bridge \
    x11-apps mesa-utils libgl1-mesa-glx libgl1-mesa-dri \
    && rm -rf /var/lib/apt/lists/*

# Configure systemd for container use
RUN systemctl set-default multi-user.target \
    && systemctl mask dev-hugepages.mount sys-fs-fuse-connections.mount \
    && systemctl mask systemd-remount-fs.service systemd-logind.service \
    && systemctl mask getty.target console-getty.service

# Copy systemd configuration
RUN mkdir -p /etc/systemd/system.conf.d
COPY system.conf /etc/systemd/system.conf.d/container.conf

# Install ROS packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-gazebo-* \
    ros-humble-joint-state-publisher \
    ros-humble-joint-state-publisher-gui \
    ros-humble-control-* \
    ros-humble-rqt-robot-steering \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && usermod -aG video,audio,dialout $USERNAME

# Configure ROS environment for all users
RUN echo 'source /opt/ros/humble/setup.bash' >> /etc/bash.bashrc \
    && echo 'if [ -f /workspace/install/setup.bash ]; then source /workspace/install/setup.bash; fi' >> /etc/bash.bashrc

# Setup entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy ROS environment service and runtime directory setup service
COPY ros-env.service /etc/systemd/system/
COPY setup-runtime-dir.service /etc/systemd/system/
RUN systemctl enable setup-runtime-dir.service

WORKDIR /workspace

# Configure systemd to work properly in container
VOLUME ["/sys/fs/cgroup"]
STOPSIGNAL SIGRTMIN+3
ENV container=docker

# Use systemd as PID 1
CMD ["/sbin/init"]

