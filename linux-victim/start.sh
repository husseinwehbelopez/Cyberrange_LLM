#!/usr/bin/env bash
set -e

# Start rsyslog and auditd (best-effort in container)
service rsyslog start || true
service auditd start || true

# Start SSH daemon in the background
/usr/sbin/sshd

# Keep container alive and show logs (auth + syslog)
touch /var/log/auth.log /var/log/syslog
tail -F /var/log/auth.log /var/log/syslog
