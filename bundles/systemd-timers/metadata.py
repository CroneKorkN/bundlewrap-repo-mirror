defaults = {
    'systemd-timers': {},
}


@metadata_reactor.provides(
    'systemd/services',
)
def services(metadata):
    return {
        'systemd': {
            'services': {
                name: {
                    'content': {
                        'Unit':{
                            'Description': f'{name} timer service',
                        },
                        'Service': {
                            'ExecStart': config['command'],
                        },
                    },
                    'enabled': False,
                    'running': False,
                } for name, config in metadata.get('systemd-timers').items() 
            },
        },
    }
