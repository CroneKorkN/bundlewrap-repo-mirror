from ipaddress import ip_interface

defaults = {
    'network': {},
}


@metadata_reactor.provides(
    'systemd/units',
)
def network_units(metadata):
    units = {}
    
    for type, network in metadata.get('network').items():
        units[f'{type}.network'] = {
            'Match': {
                'Name': network['interface'],
            },
            'Network': {
                'DHCP': 'no',
                'IPv6AcceptRA': 'no',
            }
        }
        
        for i in [4, 6]:
            if network.get(f'ipv{i}', None):
                units[f'{type}.network'].update({
                    f'Address#ipv{i}': {
                        'Address': network[f'ipv{i}'],
                    },
                })
                if f'gateway{i}' in network:
                    units[f'{type}.network'].update({
                        f'Route#ipv{i}': {
                            'Gateway': network[f'gateway{i}'],
                            'GatewayOnlink': 'yes',
                        }
                    })

    
    return {
        'systemd': {
            'units': units,
        }
    }
