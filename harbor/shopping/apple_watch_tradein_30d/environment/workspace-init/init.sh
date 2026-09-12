#!/bin/sh
set -eu
mkdir -p /target
cp -a /workspace-seed/. /target/
chmod -R a+rwX /target
