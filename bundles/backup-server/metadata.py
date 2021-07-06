from ipaddress import ip_interface

defaults = {
    'users': {
        'backup-receiver': {
            'authorized_keys': [],
        },
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
                        if other_node.metadata.get('backup/server') == node.name
                ],
            },
        },
    }
