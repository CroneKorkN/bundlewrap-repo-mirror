defaults = {
    'monitoring': {
        'services': {
            # 'test': {
            #     'vars.command': '/bin/ls /',
            #     'vars.sudo': True,
            # },
        },
    },
}


@metadata_reactor.provides(
    'monitoring/services',
)
def default_check_command(metadata):
    services = {}

    for name, conf in metadata.get('monitoring/services').items():
        services[name] = {}

        if 'host_name' not in conf:
            services[name]['host_name'] = node.name

        if 'check_command' not in conf:
            services[name]['check_command'] = 'sshmon'

    return {
        'monitoring': {
            'services': services,
        },
    }



@metadata_reactor.provides(
    'users/sshmon/authorized_users',
    'sudoers/sshmon',
)
def user(metadata):
    return {
        'users': {
            'sshmon': {
                'authorized_users': {
                    'nagios@' + metadata.get('monitoring/icinga2_node'): {},
                }
            },
        },
        'sudoers': {
            'sshmon': {
                conf['vars.command']
                    for conf in metadata.get('monitoring/services').values()
                    if conf['check_command'] == 'sshmon'
                    and conf.get('vars.sudo', None)
            },
        },
    }
