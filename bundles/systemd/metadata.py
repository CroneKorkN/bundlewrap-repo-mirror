defaults = {
    'systemd': {
        'units': {},
        'services': {},
    }
}


# create a svc_sytemd item for each .service and .timer unit
@metadata_reactor#.provides(
#    'systemd/services',
#)
def unit_services(metadata):
    services = {}
    
    for name, config in metadata.get('systemd/units').items():
        if name.split('.')[-1] not in ['timer', 'service']:
            continue
        
        services[name] = config['item']
        services[name].setdefault('needs', []).append(f"file:{config.get('path')}")

    return {
        'systemd': {
            'services': services,
        }
    }


# add defaults to units
@metadata_reactor#.provides(
#    'systemd/units',
#)
def unit_defaults(metadata):
    units = {}
    
    for name in metadata.get('systemd/units').keys():
        extension = name.split('.')[-1]

        if extension in ['netdev', 'network']:
            units[name] = {
                'path': f'/etc/systemd/network/{name}',
                'item': {
                    'triggers': [
                        'svc_systemd:systemd-networkd:restart',
                    ]
                }
            }
        elif extension in ['timer', 'service']:
            units[name] = {
                'path': f'/etc/systemd/system/{name}',
                'item': {
                    'triggers': [
                        f'svc_systemd:{name}:restart',
                    ]
                },
            }
        else:
            raise Exception(f'unknown unit extension: "{extension}"')

    return {
        'systemd': {
            'units': units,
        }
    }
