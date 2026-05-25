#!/bin/bash
set -e

echo "Starting Data Coven website application..."

cd /srv/data-coven

# shellcheck source=/dev/null
source .venv/bin/activate

cd src/apps/site

python app.py