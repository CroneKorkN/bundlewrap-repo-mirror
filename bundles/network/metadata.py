from ipaddress import ip_interface

defaults = {
    'network': {
    }
}


@metadata_reactor.provides(
    'systemd-networkd/networks',
)
def systemd_networkd(metadata):
    units = {}
    
    for type, network in metadata.get('network').items():
        units[type] = {
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
                units[type].update({
                    f'Address#ipv{i}': {
                        'Address': network[f'ipv{i}'],
                    },
                })
                if f'gateway{i}' in network:
                    units[type].update({
                        f'Route#ipv{i}': {
                            'Gateway': network[f'gateway{i}'],
                            'GatewayOnlink': 'yes',
                        }
                    })

    
    return {
        'systemd-networkd': {
            'networks': units,
        }
    }
