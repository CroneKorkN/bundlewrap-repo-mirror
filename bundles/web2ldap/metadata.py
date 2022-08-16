from importlib.metadata import metadata


defaults = {
    'apt': {
        'packages': {
            'libsasl2-dev': {},
            'python3-dev': {},
            'libldap2-dev': {},
            'libssl-dev': {},
        },
    },
}


@metadata_reactor.provides(
    'systemd/units/web2ldap.service',
)
def systemd(metadata):
    return {
        'systemd': {
            'units': {
                'web2ldap.service': {
                    'Unit': {
                        'Description': 'gitea',
                        'After': 'syslog.target',
                        'After': 'network.target',
                    },
                    'Service': {
                        'User': 'web2ldap',
                        'WorkingDirectory': '/opt/web2ldap',
                        'ExecStart': '/opt/web2ldap/bin/web2ldap 127.0.0.1 1760',
                        'Restart': 'always',
                        'Environment': [
                            '"SERVER_NAME=' + metadata.get('web2ldap/domain') + '"',
                            '"HTTP_HOST=' + metadata.get('web2ldap/domain') + '"',
                        ],
                    },
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('web2ldap/domain'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:1760',
                    }
                },
            },
        },
    }
