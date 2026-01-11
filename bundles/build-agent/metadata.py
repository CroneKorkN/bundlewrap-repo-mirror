defaults = {
    'apt': {
        'packages': {
            'build-essential': {},
            # crystal
            'clang': {},
            'libssl-dev': {},
            'libpcre3-dev': {},
            'libgc-dev': {},
            'libevent-dev': {},
            'zlib1g-dev': {},
        },
    },
    'users': {
        'build-agent': {
            'home': '/var/lib/build-agent',
        },
    },
}


@metadata_reactor.provides(
    'users/build-agent/authorized_users',
)
def ssh_keys(metadata):
    return {
        'users': {
            'build-agent': {
                'authorized_users': {
                    f'build-server@{other_node.name}': {}
                        for other_node in repo.nodes
                        if other_node.has_bundle('build-server')
                        for architecture in other_node.metadata.get('build-server/architectures').values()
                        if architecture['node'] == node.name
                },
            },
        },
    }
