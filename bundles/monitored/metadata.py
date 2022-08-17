defaults = {
    'monitoring': {
        'services': {
            'test': {
                'vars.command': '/bin/ls /',
                'host_name': node.name,
            },
        },
    },
}


@metadata_reactor.provides(
    'monitoring/services',
)
def service_defaults(metadata):
    return {
        'monitoring': {
            'services': {
                name: {
                    'check_command': 'sshmon',
                }
                    for name, conf in metadata.get('monitoring/services').items()
                    if 'check_command' not in conf
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
