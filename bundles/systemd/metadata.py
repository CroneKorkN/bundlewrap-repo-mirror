defaults = {
    'systemd': {
        'units': {},
        'services': {},
    }
}

@metadata_reactor.provides(
    'systemd/units',
)
def services(metadata):
    units = {}
    
    for name, config in metadata.get('systemd/units').items():
        if name.split('.')[-1] == 'service' and not config.get('Install/WantedBy'):
            units[name] = {
                'Install': {
                    'WantedBy': ['multi-user.target'],
                }
            }

    return {
        'systemd': {
            'units': units,
        }
    }
