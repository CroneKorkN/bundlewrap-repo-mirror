defaults = {
    'apt': {
        'packages': {
            'libgit2-dev': {},
            'libssl-dev': {},
            'cmake': {},
        },
    },
    'systemd': {
        'units': {
            'gollum.service': {
                'Unit': {
                    'Description': 'gollum',
                    'After': 'syslog.target',
                    'After': 'network.target',
                    'Requires': 'postgresql.service',
                },
                'Service': {
                    'User': 'gollum',
                    'Group': 'gollum',
                    'WorkingDirectory': '/opt/gollum',
                    'ExecStart': 'true',
                    'Restart': 'always',
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
                metadata.get('gollum/domain'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:3600',
                    }
                },
            },
        },
    }
