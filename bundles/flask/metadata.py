defaults = {
    'apt': {
        'packages': {
            'python3-pip': {},
            'python3-dev': {},
            'python3-venv': {},
        },
    },
    'flask': {},
}


@metadata_reactor.provides(
    'flask',
)
def app_defaults(metadata):
    return {
        'flask': {
            name: {
                'user': 'root',
                'group': 'root',
                'workers': 8,
                'timeout': 30,
                **conf,
            }
                for name, conf in metadata.get('flask').items()
        }
    }


@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    return {
        'systemd': {
            'units': {
                f'{name}.service': {
                    'Unit': {
                        'Description': name,
                        'After': 'network.target',
                    },
                    'Service': {
                        'Environment': {
                            f'{k}={v}'
                                for k, v in metadata.get(f'flask/{name}/env', {}).items()
                        },
                        'User': metadata.get(f'flask/{name}/user'),
                        'Group': metadata.get(f'flask/{name}/group'),
                        'ExecStart': f"/opt/{name}/venv/bin/gunicorn -w {metadata.get(f'flask/{name}/workers')} -b 127.0.0.1:{metadata.get(f'flask/{name}/port')} --timeout {metadata.get(f'flask/{name}/timeout')} {metadata.get(f'flask/{name}/app_module')}:app"
                    },
                    'Install': {
                        'WantedBy': {
                            'multi-user.target'
                        }
                    },
                }
                    for name in metadata.get('flask')
            }
        }
    }
