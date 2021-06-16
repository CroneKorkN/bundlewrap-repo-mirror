from ipaddress import ip_interface


@metadata_reactor.provides(
    'interfaces',
)
def interfaces(metadata):
    return {
        'interfaces': {
            metadata.get('network/interface'): {
                'ips': list(filter(None.__ne__, [
                    metadata.get('network/ipv4', None),
                    metadata.get('network/ipv6', None),
                ])),
                'gateway4': metadata.get('network/gateway4', None),
                'gateway6': metadata.get('network/gateway6', None),
            },
        }
    }


@metadata_reactor.provides(
    'interfaces/gateway4',
    'interfaces/gateway6',
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
