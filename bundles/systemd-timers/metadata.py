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
                'Install': {
                    'WantedBy': 'multi-user.target',
                },
            }, 
            f'{name}.service': {
                'Unit':{
                    'Description': f'{name} timer service',
                },
                'Service': {
                    'ExecStart': config['command'],
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
