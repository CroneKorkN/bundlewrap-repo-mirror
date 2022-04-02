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
                },
            },
        })
        services[f'{name}.timer'] = {}
        
    return {
        'systemd': {
            'units': units,
            'services': services,
        },
    }
