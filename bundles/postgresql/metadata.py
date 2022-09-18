import builtins


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
        'conf': {},
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
    'postgresql/conf',
)
def conf(metadata):
    conf = {}

    def limit(value, min=float('-inf'), max=float('inf'), unit=None):
        result = int(builtins.max([builtins.min([max, value]), min]))
        return str(result) + unit if unit else result

    ram = metadata.get('vm/ram', None)
    if ram:
        conf['max_connections'] = limit(ram/50, min=100)
        conf['shared_buffers'] = limit(ram/20, min=128, unit='MB')
        conf['work_mem'] = limit(ram/500, min=4, max=64, unit='MB')
        conf['temp_buffers'] = limit(ram/500, min=8, max=64, unit='MB')
        conf['effective_cache_size'] = limit(ram/3, min=4096, unit='MB')
        conf['maintenance_work_mem'] = limit(ram/50, min=64, unit='MB')

    return {
        'postgresql': {
            'conf': conf,
        },
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
                'tank/postgresql': {
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
