defaults = {
    'systemd-timers': {},
}


@metadata_reactor.provides(
    'systemd/units',
    'systemd/services',
)
def systemd(metadata):
    units = {}
    services = {}

    for name, config in metadata.get('systemd-timers').items():
        units.update({
            f'{name}.timer': {
                'Unit':{
                    'Description': f'{name} timer',
                },
                'Timer': {
                    'OnCalendar': config['when'],
                    'Persistent': config.get('persistent', False),
                    'Unit': f'{name}.service',
                },
            },
            f'{name}.service': {
                'Unit':{
                    'Description': f'{name} timer service',
                },
                'Service': {
                    'User': config.get('user', 'root'),
                    'ExecStart': config['command'],
                    'Environment': config.get('env'),
                    'Nice': config.get('nice', 10),
                },
            },
        })
        if config.get('working_dir'):
            units[f'{name}.service']['Service']['WorkingDirectory'] = config['working_dir']
        if config.get('success_exit_status'):
            units[f'{name}.service']['Service']['SuccessExitStatus'] = config['success_exit_status']

        services[f'{name}.timer'] = {}

    return {
        'systemd': {
            'units': units,
            'services': services,
        },
    }


@metadata_reactor.provides(
    'monitoring/services',
)
def monitoring(metadata):
    return {
        'monitoring': {
            'services': {
                f'{name}.timer': {
                    'vars.command': f'/usr/lib/nagios/plugins/check_systemd_timer {name}'
                }
                    for name in metadata.get('systemd-timers')
            },
        },
    }
