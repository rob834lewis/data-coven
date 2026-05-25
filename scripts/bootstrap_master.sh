#!/bin/bash

# this setting will cause the script to exit immediately if any command exits with a non-zero status
set -e

echo "Starting Data Coven bootstrap..."

# make all shell scripts executable
chmod +x scripts/*.sh

# configure coven user
bash scripts/bootstrap_user.sh

# install Python and dependencies
sudo -u coven bash scripts/bootstrap_python.sh

echo "Data Coven bootstrap complete."

# start application
sudo -u coven bash scripts/startup.sh

