root_password = repo.vault.password_for(f'{node.name} postgresql root')

defaults = {
    'apt': {
        'packages': {
            'postgresql': {},
        },
    },
    'backup': {
        'paths': {
            '/var/lib/postgresql',
        },
    },
    'postgresql': {
        'roles': {
            'root': {
                'password': root_password,
                'superuser': True,
            },
        },
        'databases': {},
    },
    'grafana_rows': set(),
}

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'datasets': {
            'tank/postgresql': {
                'mountpoint': '/var/lib/postgresql',
                'recordsize': '8192',
                'atime': 'off',
                'logbias': 'throughput',
            },
        },
    }


@metadata_reactor.provides(
    'telegraf/config/inputs/postgresql',
)
def telegraf(metadata):
    return {
        'telegraf': {
            'config': {
                'inputs': {
                    'postgresql': [{
                        'address': f'postgres://root:{root_password}@localhost:5432/postgres',
                        'databases': sorted(list(node.metadata.get('postgresql/databases').keys())),
                    }],
                },
            },
        },
    }
