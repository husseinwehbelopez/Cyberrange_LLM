FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    gnupg \
    lsb-release \
    sudo \
    openssh-server \
    rsyslog \
    auditd \
    python3 \
    python3-pip \
    jq \
    vim \
    net-tools \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Basic SSH setup (root:toor for lab only!)
RUN mkdir /var/run/sshd && \
    echo 'root:toor' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Install PowerShell Core (for Invoke-AtomicRedTeam)
RUN wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb && \
    dpkg -i /tmp/packages-microsoft-prod.deb && \
    rm /tmp/packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y powershell && \
    rm -rf /var/lib/apt/lists/*

# Install Invoke-AtomicRedTeam PowerShell module
RUN pwsh -Command "Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted; \
    Install-Module -Name Invoke-AtomicRedTeam -Scope AllUsers -Force"

# Clone Atomic Red Team repo (Linux tests live here)
RUN git clone https://github.com/redcanaryco/atomic-red-team.git /opt/atomic-red-team

# Startup script to kick off logging services and keep container alive
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
