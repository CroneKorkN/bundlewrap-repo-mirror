defaults = {
    'apt': {
        'packages': {
            'wakeonlan': {},
        },
    },
}

@metadata_reactor.provides(
    'users/wol',
)
def user(metadata):
    return {
        'users': {
            'wol': {
                'authorized_users': {
                    f'root@{node.name}'
                        for node in repo.nodes
                        if node.dummy == False
                },
            },
        },
    }
