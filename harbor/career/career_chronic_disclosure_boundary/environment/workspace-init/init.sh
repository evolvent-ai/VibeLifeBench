#!/bin/sh
set -eu
mkdir -p /target
find /target -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
cp -a /seed/. /target/
find /target -type f -exec chmod 0644 {} +
printf '%s\n' 'workspace initialized'
