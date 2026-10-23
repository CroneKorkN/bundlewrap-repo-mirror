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
    sleepers = [
        sleeper
            for sleeper in repo.nodes
            if sleeper.has_bundle('wol-sleeper')
            and sleeper.metadata.get('wol-sleeper/waker') == node.name
    ]
    commands = {
        sleeper.metadata.get('wol-sleeper/waker_command')
            for sleeper in sleepers
    }
    # icinga wakes sleepers before checks that need them awake
    clients = {
        f'root@{ssh_client.name}'
            for ssh_client in repo.nodes
            if ssh_client.dummy == False and ssh_client.has_bundle('ssh')
    } | {
        f"nagios@{sleeper.metadata.get('monitoring/icinga2_node')}"
            for sleeper in sleepers
            if sleeper.has_bundle('monitored')
    }

    return {
        'users': {
            'wol': {
                'authorized_users': {
                    client: {
                        'commands': commands,
                    }
                        for client in clients
                },
            },
        },
    }
