defaults = {
    'systemd': {
        'units': {},
        'services': {},
        'logind': {},
    }
}

@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    units = {}
    
    for name, config in metadata.get('systemd/units').items():
        if '/' in name:
            continue

        type = name.split('.')[-1]

        if type not in ['timer', 'service', 'network', 'netdev', 'mount', 'swap']:
            raise Exception(f'unknown type {type}')

        if not config.get('Install/WantedBy'):
            if type == 'service':
                units[name] = {
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    }
                }
            elif type == 'timer':
                units[name] = {
                    'Install': {
                        'WantedBy': {'timers.target'},
                    }
                }

    return {
        'systemd': {
            'units': units,
        }
    }


@metadata_reactor.provides(
    'systemd/services',
)
def services(metadata):
    services = {}
    
    for name, config in metadata.get('systemd/services').items():
        extension = name.split('.')[-1]
        
        if extension not in ['timer', 'service', 'mount', 'swap']:
            raise Exception(f'unknown extension: {extension}')

    return {
        'systemd': {
            'services': services,
        }
    }
