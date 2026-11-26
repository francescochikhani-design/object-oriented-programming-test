#!/usr/bin/env bash
set -euo pipefail

case "${1:-}" in
    --dry-run) printf '%s\n' 'sudo apt-get update' 'sudo apt-get install -y tree'; exit 0 ;;
    '') ;;
    *) printf '%s\n' 'Usage: bash install.sh [--dry-run]' >&2; exit 2 ;;
esac
printf '%s\n' 'Starting installation...'
sudo apt-get update
sudo apt-get install -y tree
printf '%s\n' 'Installation complete!'
