#!/bin/bash
set -e

# WARNING: SSH and cron are started for DEVELOPMENT ONLY.
# This allows SSH access for debugging and loading cron tasks.
# DO NOT use in production.

# Start SSH server for development backdoor
/usr/sbin/sshd

# Start cron for task scheduling
cron

# Load config if exists
if [ -f /app/config/config.yaml ]; then
    export CONFIG_FILE=/app/config/config.yaml
fi

# Start the vault service
exec python src/main.py