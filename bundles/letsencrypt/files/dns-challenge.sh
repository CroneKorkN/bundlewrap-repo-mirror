#!/usr/bin/env bash

set -e
set -u
set -o pipefail

OPERATION=$1
DOMAIN=$2
TOKEN=$4
TTL=300

case "$1" in
  "deploy_challenge")
    
    ;;
  "clean_challenge")
    ;;
  "deploy_cert")
    ;;
  "unchanged_cert")
    ;;
  "startup_hook")
    ;;
  "exit_hook")
    ;;
esac

exit 0
