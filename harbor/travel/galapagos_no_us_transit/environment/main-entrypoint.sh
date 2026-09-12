#!/bin/sh
set -eu

# Harbor injects a host HTTP proxy into every container. Internal service names
# must bypass that proxy so setup scripts can reach world-controller directly.
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
unset NO_PROXY no_proxy

exec "$@"
