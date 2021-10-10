from ipaddress import ip_network, ip_interface


@metadata_reactor.provides(
    'systemd/units',
)
def network(metadata):
    interface = ip_interface(metadata.get('network/internal/ipv4'))
    network = ip_interface(f'{interface.ip}/24').network
    gateway = network[1]
    
    return {
        'systemd': {
            'units': {
                'internal.network': {
                    f'Route#hetzner_gateway': {
                        'Destination': str(gateway),
                        'Scope': 'link',
                    },
                    f'Route#hetzner_network': {
                        'Destination': str(network),
                        'Gateway': str(gateway),
                    },
                },
            },
        },
    }
