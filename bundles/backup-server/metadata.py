from ipaddress import ip_interface


@metadata_reactor.provides(
    'users/backup-receiver/authorized_keys'
)
def backup_authorized_keys(metadata):
    authorized_keys = []
    
    for other_node in repo.nodes:
        if other_node.metadata.get('backup/server') == node.name:
            authorized_keys.append(other_node.metadata.get('users/root/pubkey'))
        
    return {
        'users': {
            'backup-receiver': {
                'authorized_keys': authorized_keys,
            },
        },
    }
