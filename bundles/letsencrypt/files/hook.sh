deploy_challenge() {
  set -e
  set -u
  set -o pipefail
  
  ACME_ZONE=${zone}
  SERVER=${server}
  DOMAIN=$1
  CHALLENGE=$3
  KEY=hmac-sha512:acme.sublimity.de:${acme_key}
  cmd="
    server 162.55.188.157
    zone acme.sublimity.de.
    update add $DOMAIN.$ACME_ZONE. 60 IN TXT \"$CHALLENGE\"
    send
  "
  echo "$cmd"
  echo "$cmd" | nsupdate -y $KEY
  
  sleep 15
}

clean_challenge() {
  set -e
  set -u
  set -o pipefail
  
  ACME_ZONE=${zone}
  SERVER=${server}
  DOMAIN=$1
  CHALLENGE=$3
  KEY=hmac-sha512:acme.sublimity.de:${acme_key}
  cmd="
    server 162.55.188.157
    zone acme.sublimity.de.
    update delete $DOMAIN.$ACME_ZONE. TXT
    send
  "
  echo "$cmd"
  echo "$cmd" | nsupdate -y $KEY
}

deploy_cert() {<%text>
    local DOMAIN="${1}" KEYFILE="${2}" CERTFILE="${3}" FULLCHAINFILE="${4}" CHAINFILE="${5}" TIMESTAMP="${6}"</%text>
% for service, config in node.metadata.get('letsencrypt/concat_and_deploy', {}).items():

    # concat_and_deploy ${service}
    if [ "$DOMAIN" = "${config['match_domain']}" ]; then
        cat $KEYFILE > ${config['target']}
        cat $FULLCHAINFILE >> ${config['target']}
%  if 'chown' in config:
        chown ${config['chown']} ${config['target']}
%  endif
%  if 'chmod' in config:
        chmod ${config['chmod']} ${config['target']}
%  endif
%  if 'commands' in config:
%   for command in config['commands']:
        ${command}
%   endfor
%  endif
    fi
% endfor
}


exit_hook() {<%text>
    local ERROR="${1:-}"</%text>

% for service in sorted(node.metadata.get('letsencrypt/reload_after', set())):
    systemctl reload-or-restart ${service}
% endfor
}

<%text>
HANDLER="$1"; shift
if [[ "${HANDLER}" =~ ^(deploy_cert|exit_hook|deploy_challenge|clean_challenge)$ ]]; then
    "$HANDLER" "$@"
fi</%text>
