FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/redteam

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    git \
    gnupg \
    lsb-release \
    python3 \
    python3-pip \
    less \
    nano \
    iproute2 \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Install PowerShell Core (per Microsoft docs for Ubuntu 22.04)
RUN wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y powershell && \
    rm -rf /var/lib/apt/lists/*

# Pull Invoke-AtomicRedTeam from PowerShell Gallery
# Docs: 'Install-Module -Name Invoke-AtomicRedTeam':contentReference[oaicite:5]{index=5}
RUN pwsh -Command "Set-PSRepository -Name 'PSGallery' -InstallationPolicy Trusted; \
    Install-Module -Name Invoke-AtomicRedTeam -Scope AllUsers -Force"

# Optionally clone the atomic tests repo (atomics folder, markdown, etc.):contentReference[oaicite:6]{index=6}
RUN git clone https://github.com/redcanaryco/atomic-red-team.git /opt/redteam/atomic-red-team

COPY run_example_tests.ps1 /opt/redteam/run_example_tests.ps1

CMD [ "pwsh" ]

