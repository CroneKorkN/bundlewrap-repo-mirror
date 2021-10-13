defaults = {
    'systemd': {
        'units': {},
        'services': {},
    }
}

@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    units = {}
    
    for name, config in metadata.get('systemd/units').items():
        extension = name.split('.')[-1]

        if extension not in ['timer', 'service', 'network', 'netdev']:
            raise Exception(f'unknown extension {extension}')

        if not config.get('Install/WantedBy'):
            if extension == 'service':
                units[name] = {
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    }
                }
            elif extension == 'timer':
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
        
        if extension not in ['timer', 'service']:
            raise Exception(f'unknown extension: {extension}')

    return {
        'systemd': {
            'services': services,
        }
    }
