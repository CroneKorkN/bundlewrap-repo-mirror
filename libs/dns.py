from ipaddress import ip_interface

def get_a_records(metadata, internal=True, external=True):
    networks = metadata.get('network')
    
    if not internal:
        networks.pop('internal')

    if not external:
        networks.pop('external')
    
    return {
        'A': [
            str(ip_interface(network['ipv4']).ip)
                for network in networks.values()
                if 'ipv4' in network
        ],
        'AAAA': [
            str(ip_interface(network['ipv6']).ip)
                for network in networks.values()
                if 'ipv6' in network
        ],
    }
