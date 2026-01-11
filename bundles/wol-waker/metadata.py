defaults = {
    'apt': {
        'packages': {
            'wakeonlan': {},
        },
    },
}


@metadata_reactor.provides(
    'users/wol/authorized_users',
)
def user(metadata):
    return {
        'users': {
            'wol': {
                'authorized_users': {
                    f'root@{ssh_client.name}': {
                        'commands': {
                            '/usr/bin/wakeonlan ' + sleeper.metadata.get('wol-sleeper/mac')
                                for sleeper in repo.nodes
                                if sleeper.has_bundle('wol-sleeper')
                                and sleeper.metadata.get('wol-sleeper/waker') == node.name
                        }
                    }
                        for ssh_client in repo.nodes
                        if ssh_client.dummy == False and ssh_client.has_bundle('ssh')
                },
            },
        },
    }
