import builtins


root_password = repo.vault.password_for(f'{node.name} postgresql root')

defaults = {
    'apt': {
        'packages': {
            'postgresql': {
                'needs': {
                    'zfs_dataset:tank/postgresql',
                },
            },
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

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'datasets': {
            'tank/postgresql': {
                'mountpoint': '/var/lib/postgresql',
                # 16k compresses better than the 8k pages, copy on write makes partial page writes cheap
                'recordsize': '16384',
                'atime': 'off',
            },
        },
    }
    # copy on write never tears a page and never reuses wal blocks in place
    defaults['postgresql']['conf'] = {
        'full_page_writes': 'off',
        'wal_init_zero': 'off',
        'wal_recycle': 'off',
        # random reads are served from the arc or ssds
        'random_page_cost': '1.1',
    }


@metadata_reactor.provides(
    'postgresql/conf',
)
def conf(metadata):
    conf = {
        # jit compilation only pays off for long analytical queries
        'jit': 'off',
    }

    def limit(value, min=float('-inf'), max=float('inf'), unit=None):
        result = int(builtins.max([builtins.min([max, value]), min]))
        return str(result) + unit if unit else result

    ram = metadata.get('vm/ram', None)
    if ram:
        conf['max_connections'] = limit(ram/50, min=100, max=200)
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
    'apt/config/APT/NeverAutoRemove',
)
def apt(metadata):
    return {
        'apt': {
            'config': {
                'APT': {
                    'NeverAutoRemove': {
                        # https://github.com/credativ/postgresql-common/blob/master/pg_updateaptconfig#L17-L21
                        f"^postgresql.*-{metadata.get('postgresql/version')}",
                    },
                },
            },
        },
    }



@metadata_reactor.provides(
    'telegraf/inputs/postgresql/default',
)
def telegraf(metadata):
    return {
        'telegraf': {
            'inputs': {
                'postgresql': {
                    'default': {
                        'address': f'postgres://root:{root_password}@localhost:5432/postgres',
                        'databases': sorted(list(node.metadata.get('postgresql/databases').keys())),
                    },
                },
            },
        },
    }
