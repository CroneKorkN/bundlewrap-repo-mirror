from ipaddress import ip_interface


@metadata_reactor.provides(
    'interfaces',
)
def interfaces(metadata):
    interface = {
        'ips': [],
    }
    
    if metadata.get('network/ipv4', None):
        interface['ips'].append(metadata.get('network/ipv4'))
        interface['gateway4'] = metadata.get('network/gateway4')
    
    if metadata.get('network/ipv6', None):
        interface['ips'].append(metadata.get('network/ipv6'))
        interface['gateway6'] = metadata.get('network/gateway6')
    
    return {
        'interfaces': {
            metadata.get('network/interface'): interface,
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
