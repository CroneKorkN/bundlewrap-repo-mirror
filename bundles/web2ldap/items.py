from shlex import quote

users = {
    'web2ldap': {},
}

directories = {
    '/opt/web2ldap': {
        'owner': 'web2ldap',
    },
}

actions = {
    'web2ldap_initialize_venv': {
        'command': 'sudo -u web2ldap python3 -m venv /opt/web2ldap',
        'unless': 'test -e /opt/web2ldap/bin/pip3',
        'needs': [
            'directory:/opt/web2ldap',
        ],
        'triggers': [
            'svc_systemd:web2ldap.service:restart',
        ],
    },
    'web2ldap_install': {
        'command': """sudo -u web2ldap /opt/web2ldap/bin/pip3 install web2ldap""",
        'unless': """sudo -u web2ldap /opt/web2ldap/bin/pip3 list --format=freeze | cut -d '=' -f 1 | grep -q '^web2ldap$'""",
        'needs': [
            'action:web2ldap_initialize_venv',
        ],
        'triggers': [
            'svc_systemd:web2ldap.service:restart',
        ],
    },
    'web2ldap_set_cookie_domain': {
        'command': f"""sed -iE "s/^cookie_domain.*/cookie_domain = '{node.metadata.get('web2ldap/domain')}'/g" /opt/web2ldap/etc/web2ldap/web2ldapcnf/__init__.py""",
        'unless':  f"""grep -q "^cookie_domain = '{node.metadata.get('web2ldap/domain')}'$" /opt/web2ldap/etc/web2ldap/web2ldapcnf/__init__.py""",
        'needs': [
            'action:web2ldap_install',
        ],
        'triggers': [
            'svc_systemd:web2ldap.service:restart',
        ],
    },
    'web2ldap_upgrade_venv': {
        'command': """sudo -u web2ldap /opt/web2ldap/bin/pip3 list --outdated --format=freeze | cut -d '=' -f 1 | xargs -n1 /opt/web2ldap/bin/pip3 install --upgrade""",
        'unless':  """sudo -u web2ldap /opt/web2ldap/bin/pip3 list --outdated --format=freeze | wc -l | grep -q '^0$'""",
        'needs': [
            'action:web2ldap_install',
        ],
        'triggers': [
            'svc_systemd:web2ldap.service:restart',
        ],
    },
}

svc_systemd = {
    'web2ldap.service': {
        'needs': [
            'action:web2ldap_initialize_venv',
            'action:web2ldap_upgrade_venv',
        ],
    },
}
