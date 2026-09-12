#!/bin/sh
set -eu

mkdir -p /target
# workspace-init is a one-shot initializer. Keep the copy deterministic and
# include dotfiles without following links supplied by a seed.
find /target -mindepth 1 -maxdepth 1 -exec rm -rf -- {} +
cp -a /seed/. /target/
find /target -type f -exec chmod 0644 {} +
printf '%s\n' 'graduate exam preparation workspace initialized'
