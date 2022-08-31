set -e
set -u
set -o pipefail

deploy_challenge() {
  echo "
    server 10.0.11.3
    zone ${zone}.
    update add $1.${zone}. 60 IN TXT \"$3\"
    send
  " | tee | nsupdate -y hmac-sha512:${acme_key_name}:${acme_key}
}

clean_challenge() {
  echo "
    server 10.0.11.3
    zone ${zone}.
    update delete $1.${zone}. TXT
    send
  " | tee | nsupdate -y hmac-sha512:${acme_key_name}:${acme_key}
}

deploy_cert() {
  DOMAIN="$1"
  KEYFILE="$2"
  CERTFILE="$3"
  FULLCHAINFILE="$4"
  CHAINFILE="$5"

  case $DOMAIN in
  % for domain, conf in sorted(domains.items()):
<%   if not conf: continue %>\
    ${domain})
      % if conf.get('location', None):
      cat "$KEYFILE" > "${conf['location']}/${conf.get('privkey_name', 'privkey.pem')}"
      cat "$CERTFILE" > "${conf['location']}/${conf.get('cert_name', 'cert.pem')}"
      cat "$FULLCHAINFILE" > "${conf['location']}/${conf.get('fullchain_name', 'fullchain.pem')}"
      cat "$CHAINFILE" > "${conf['location']}/${conf.get('chain_name', 'chain.pem')}"
      % endif
      % if conf.get('owner', None):
      chown ${conf['owner']}:${conf.get('group', '')} \
        "${conf['location']}/${conf.get('privkey_name', 'privkey.pem')}" \
        "${conf['location']}/${conf.get('cert_name', 'cert.pem')}" \
        "${conf['location']}/${conf.get('fullchain_name', 'fullchain.pem')}" \
        "${conf['location']}/${conf.get('chain_name', 'chain.pem')}"
      % endif
      % for service in sorted(conf.get('reload', [])):
      systemctl reload-or-restart ${service}
      % endfor
      % for service in sorted(conf.get('start', [])):
      systemctl start ${service}
      % endfor
    ;;
  % endfor
  esac
}

HANDLER="$1"; shift
if [[ $HANDLER =~ ^(deploy_cert|deploy_challenge|clean_challenge)$ ]]
then
    "$HANDLER" "$@"
fi
