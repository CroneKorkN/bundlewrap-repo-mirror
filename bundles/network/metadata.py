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


@metadata_reactor.provides(
    'network/gateway4',
    'network/gateway6',
)
def guess_gateway(metadata):
    networks = {}
    
    for type, network in metadata.get('network').items():
        if not network.get('gateway4', None):
            if ip_interface(network['ipv4']).network.prefixlen == 32:
                networks[type] = {
                    'gateway4': str(ip_interface(network['ipv4']).network[0]),
                }
            else:
                networks[type] = {
                    'gateway4': str(ip_interface(network['ipv4']).network[1]),
                }
    
    return {
        'network': networks,
    }
