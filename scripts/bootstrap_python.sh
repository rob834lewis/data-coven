#!/bin/bash
set -e

echo "Installing Python 3.14.5..."

apt-get update

apt-get install -y \
build-essential \
wget \
curl \
libssl-dev \
zlib1g-dev \
libbz2-dev \
libreadline-dev \
libsqlite3-dev \
libffi-dev \
libncurses-dev \
libgdbm-dev \
liblzma-dev \
tk-dev \
uuid-dev

cd /tmp

wget https://www.python.org/ftp/python/3.14.5/Python-3.14.5.tgz

tar -xzf Python-3.14.5.tgz

cd Python-3.14.5

./configure \
    --enable-optimizations

make -j"$(nproc)"

make altinstall

echo "Python installed"

python3.14 --version

cd /srv/data-coven

echo "Creating .venv"

python3.14 -m venv .venv

# shellcheck source=/dev/null
source .venv/bin/activate

pip install --upgrade pip

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

deactivate

echo "Python bootstrap complete"