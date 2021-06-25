from ipaddress import ip_interface

defaults = {
    'users': {
        'backup-receiver': {
            'authorized_keys': [],
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
            datasets[f"tank/{other_node.metadata.get('id')}/fs"] = {
                'mountpoint': f"/mnt/backups/{other_node.metadata.get('id')}",
                'backup': False,
            }

    return {
        'zfs': {
            'datasets': datasets,
        },
    }


@metadata_reactor.provides(
    'dns'
)
def dns(metadata):
    records = {}
    
    if metadata.get('network/ipv4', None):
        records['A'] = [str(ip_interface(metadata.get('network/ipv4')).ip)]
    if metadata.get('network/ipv6', None):
        records['AAAA'] = [str(ip_interface(metadata.get('network/ipv6')).ip)]

    return {
        'dns': {
            metadata.get('backup-server/hostname'): records,
        },
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
