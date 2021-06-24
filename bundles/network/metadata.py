from ipaddress import ip_interface


@metadata_reactor.provides(
    'systemd-networkd/networks',
)
def interfaces(metadata):
    network = {
        'Match': {
            'Name': metadata.get('network/interface'),
        },
        'Network': {
            'DHCP': 'no',
            'IPv6AcceptRA': 'no',
        }
    }
    
    for i in [4, 6]:
        if metadata.get(f'network/ipv{i}', None):
            network.update({
                f'Address#ipv{i}': {
                    'Address': metadata.get(f'network/ipv{i}'),
                },
                f'Route#ipv{i}': {
                    'Gateway': metadata.get(f'network/gateway{i}'),
                    'GatewayOnlink': 'yes',
                }
            })
    
    return {
        'systemd-networkd': {
            'networks': {
                metadata.get('network/interface'): network,
            }
        }
    }


@metadata_reactor.provides(
    'network/gateway4',
    'network/gateway6',
)
def guess_gateway(metadata):
    if metadata.get('network/gateway4', None):
        return {}
    else:
        return {
            'network': {
                'gateway4': str(
                    ip_interface(metadata.get('network/ipv4')).network[1]
                ),
            }
        }
