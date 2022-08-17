defaults = {
    'monitoring': {
        'services': {
            'test': {
                'vars.command': '/bin/ls /',
                'check_command': 'sshmon',
                'host_name': node.name,
            },
        },
    },
}

@metadata_reactor.provides(
    'users/sshmon/authorized_users'
)
def user(metadata):
    return {
        'users': {
            'sshmon': {
                'authorized_users': {
                    'nagios@' + metadata.get('monitoring/icinga2_node'),
                }
            },
        },
    }
