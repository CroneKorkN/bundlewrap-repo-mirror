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
                    other_node.metadata.get('users/backup/pubkey')
                        for other_node in repo.nodes
                        if other_node.has_bundle('backup')
                        and other_node.metadata.get('backup/server') == node.name
                ],
            },
        },
    }
