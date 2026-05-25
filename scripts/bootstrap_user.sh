#!/bin/bash

# this setting will cause the script to exit immediately if any command exits with a non-zero status
set -e

echo "Configuring coven user..."

# Create user if missing
if id "coven" >/dev/null 2>&1; then
    echo "User coven already exists."
else
    useradd -m -s /bin/bash coven
    echo "User coven created."
fi

# Add to sudo group
usermod -aG sudo coven

# Transfer ownership
chown -R coven:coven /srv/data-coven

echo "Coven user configuration complete."