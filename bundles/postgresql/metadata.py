from importlib.metadata import metadata


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


@metadata_reactor.provides(
    'zfs/datasets',
)
def zfs(metadata):
    if not node.has_bundle('zfs'):
        return {}

    return {
        'zfs': {
            'datasets': {
                f"{metadata.get('zfs/storage_classes/ssd')}/postgresql": {
                    'mountpoint': '/var/lib/postgresql',
                    'recordsize': '8192',
                    'atime': 'off',
                },
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
