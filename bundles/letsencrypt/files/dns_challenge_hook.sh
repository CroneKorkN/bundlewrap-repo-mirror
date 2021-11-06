#!/usr/bin/env bash

set -e
set -u
set -o pipefail

ACME_ZONE=${acme_hostname}
SERVER=${bind_hostname}
OPERATION=$1
DOMAIN=$2
TOKEN=$4
TTL=300

case "$1" in
  "deploy_challenge")
    printf "
      server 127.0.0.1
      zone $ACME_ZONE.
      update add $DOMAIN.$ACME_ZONE. 600 IN TXT \"$TOKEN\"
      send
    " | nsupdate -y $TOKEN
    ;;
  "clean_challenge")
    printf "
      server 127.0.0.1
      zone $ACME_ZONE.
      update delete $DOMAIN.$ACME_ZONE. TXT
      send
    " | nsupdate -y $TOKEN
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
