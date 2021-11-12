from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'rsync': {},
        },
    },
    'users': {
        'backup-receiver': {
            'authorized_keys': set(),
        },
    },
    'sudoers': {
        'backup-receiver': ['ALL'],
    }
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
            base_dataset = f"tank/{other_node.metadata.get('id')}"

            # container
            datasets[base_dataset] = {
                'mountpoint': None,
                'readonly': 'on',
                'backup': False,
                'com.sun:auto-snapshot': 'false',
            }
            
            # for rsync backups
            datasets[f'{base_dataset}/fs'] = {
                'mountpoint': f"/mnt/backups/{other_node.metadata.get('id')}",
                'readonly': 'off',
                'backup': False,
                'com.sun:auto-snapshot': 'true',
            }
            
            # for zfs send/recv
            if other_node.has_bundle('zfs'):
                
                # base datasets for each tank
                for pool in other_node.metadata.get('zfs/pools'):
                    datasets[f'{base_dataset}/{pool}'] = {
                        'mountpoint': None,
                        'readonly': 'on',
                        'backup': False,
                        'com.sun:auto-snapshot': 'false',
                    }
                
                # actual datasets
                for path in other_node.metadata.get('backup/paths'):
                    for dataset, config in other_node.metadata.get('zfs/datasets').items():
                        if path == config.get('mountpoint'):
                            datasets[f'{base_dataset}/{dataset}'] = {
                                'mountpoint': None,
                                'readonly': 'on',
                                'backup': False,
                                'com.sun:auto-snapshot': 'false',
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
            metadata.get('backup-server/hostname'): repo.libs.dns.get_a_records(metadata),
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
