from ipaddress import ip_interface

defaults = {
    'users': {
        'backup-receiver': {
            'authorized_keys': [],
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
            datasets[f"tank/{other_node.metadata.get('id')}/fs"] = {
                'mountpoint': f"/mnt/backups/{other_node.metadata.get('id')}",
                'backup': False,
            }
            
            if other_node.has_bundle('zfs'):
                for path in other_node.metadata.get('backup/paths'):
                    for dataset, config in other_node.metadata.get('zfs/datasets').items():
                        if path == config.get('mountpoint'):
                            datasets[f"tank/{other_node.metadata.get('id')}/{dataset}"] = {
                                'mountpoint': 'none',
                                'readonly': 'on',
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
                'authorized_keys': [
                    other_node.metadata.get('users/root/pubkey')
                        for other_node in repo.nodes
                        if other_node.has_bundle('backup')
                        and other_node.metadata.get('backup/server') == node.name
                ],
            },
        },
    }
