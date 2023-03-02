from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'rsync': {},
        },
    },
    'backup-receiver': {
        'datasets': {},
    },
    'monitoring': {
        'services': {
            'backup freshness': {
                'vars.command': '/usr/lib/nagios/plugins/check_backup_freshness',
                'check_interval': '6h',
                'vars.sudo': True,
            },
        },
    },
    'users': {
        'backup-receiver': {
            'authorized_keys': set(),
        },
    },
    'sudoers': {
        'backup-receiver': {
            '/usr/bin/rsync',
            '/sbin/zfs',
        },
    },
    'zfs': {
        'datasets': {
            'tank': {
                'recordsize': "1048576",
            },
        },
    },
}


@metadata_reactor.provides(
    'zfs/datasets'
)
def zfs(metadata):
    datasets = {}

    for other_node in repo.nodes:
        if (
            other_node.has_bundle('backup') and
            other_node.metadata.get('backup/server') == node.name
        ):
            id = other_node.metadata.get('id')
            base_dataset = f'tank/{id}'

            # container
            datasets[base_dataset] = {
                'mountpoint': None,
                'readonly': 'on',
                'compression': 'lz4',
                'com.sun:auto-snapshot': 'false',
                'backup': False,
            }

            # for rsync backups
            datasets[f'{base_dataset}/fs'] = {
                'mountpoint': f"/mnt/backups/{id}",
                'readonly': 'off',
                'compression': 'lz4',
                'com.sun:auto-snapshot': 'true',
                'backup': False,
            }

            # for zfs send/recv
            if other_node.has_bundle('zfs'):

                # base datasets for each tank
                for pool in other_node.metadata.get('zfs/pools'):
                    datasets[f'{base_dataset}/{pool}'] = {
                        'mountpoint': None,
                        'readonly': 'on',
                        'compression': 'lz4',
                        'com.sun:auto-snapshot': 'false',
                        'backup': False,
                    }

                # actual datasets
                for path in other_node.metadata.get('backup/paths'):
                    for dataset, config in other_node.metadata.get('zfs/datasets').items():
                        if path == config.get('mountpoint'):
                            datasets[f'{base_dataset}/{dataset}'] = {
                                'mountpoint': None,
                                'readonly': 'on',
                                'compression': 'lz4',
                                'com.sun:auto-snapshot': 'false',
                                'backup': False,
                            }
                            continue

    return {
        'zfs': {
            'datasets': datasets,
        },
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('backup-server/hostname'): repo.libs.ip.get_a_records(metadata),
        }
    }


@metadata_reactor.provides(
    'users/backup-receiver/authorized_keys'
)
def backup_authorized_keys(metadata):
    return {
        'users': {
            'backup-receiver': {
                'authorized_keys': {
                    other_node.metadata.get('users/root/pubkey')
                        for other_node in repo.nodes
                        if other_node.has_bundle('backup')
                        and other_node.metadata.get('backup/server') == node.name
                },
            },
        },
    }


@metadata_reactor.provides(
    'backup-receiver/datasets'
)
def check_datasets(metadata):
    return {
        'backup-receiver': {
            'datasets': {
                f"{other_node.metadata.get('id')}/{dataset}"
                    for other_node in repo.nodes
                    if other_node.has_bundle('backup')
                    and other_node.has_bundle('zfs')
                    and other_node.metadata.get('backup/server') == node.name
                    for dataset, options in other_node.metadata.get('zfs/datasets').items()
                    if options.get('backup', True)
                    and not options.get('mountpoint', None) in [None, 'none']
            },
        },
    }
