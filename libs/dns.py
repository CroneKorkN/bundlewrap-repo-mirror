from ipaddress import ip_interface

def get_a_records(metadata):
    return {
        'A': [
            str(ip_interface(network['ipv4']).ip)
                for network in metadata.get('network').values()
                if 'ipv4' in network
        ],
        'AAAA': [
            str(ip_interface(network['ipv6']).ip)
                for network in metadata.get('network').values()
                if 'ipv6' in network
        ],
    }
