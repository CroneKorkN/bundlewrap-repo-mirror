set -e
set -u
set -o pipefail

deploy_challenge() {
  echo "
    server ${server}
    zone ${zone}.
    update add $1.${zone}. 60 IN TXT \"$3\"
    send
  " | tee | nsupdate -y hmac-sha512:${zone}:${acme_key}
  
  sleep 10
}

clean_challenge() {
  echo "
    server ${server}
    zone ${zone}.
    update delete $1.${zone}. TXT
    send
  " | tee | nsupdate -y hmac-sha512:${zone}:${acme_key}
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
      cat "$KEYFILE" > "${conf['location']}/privkey.pem"
      cat "$CERTFILE" > "${conf['location']}/cert.pem"
      cat "$FULLCHAINFILE" > "${conf['location']}/fullchain.pem"
      cat "$CHAINFILE" > "${conf['location']}/chain.pem"
      % endif
      % if conf.get('owner', None):
      chown ${conf['owner']} "${conf['location']}/privkey.pem" "${conf['location']}/cert.pem" "${conf['location']}/fullchain.pem" "${conf['location']}/chain.pem"
      % endif
      % for service in sorted(conf.get('reload', [])):
      systemctl reload-or-restart ${service}
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
