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
