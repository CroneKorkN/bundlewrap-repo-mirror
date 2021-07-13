defaults = {
    'systemd-timers': {},
}


@metadata_reactor.provides(
    'systemd/services',
)
def timers(metadata):
    return {
        'systemd': {
            'units': {
                f'{name}.timer': {
                    'content': {
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
                        }
                    },
                } for name, config in metadata.get('systemd-timers').items()
            },
        },
    }


@metadata_reactor.provides(
    'systemd/services',
)
def services(metadata):
    return {
        'systemd': {
            'units': {
                f'{name}.service': {
                    'content': {
                        'Unit':{
                            'Description': f'{name} timer service',
                        },
                        'Service': {
                            'ExecStart': config['command'],
                        },
                    },
                    'item': {
                        'enabled': False,
                        'running': False,
                    },
                } for name, config in metadata.get('systemd-timers').items()
            },
        },
    }
