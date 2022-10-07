from ipaddress import ip_address, ip_interface


def get_a_records(metadata, internal=True, external=True):
    networks = metadata.get('network')

    if not internal:
        networks.pop('internal', None)

    if not external:
        networks.pop('external', None)

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


def get_all_ips(nodes):
    ips = set()

    for node in nodes:
        try:
            ip_address(node.hostname)
        except ValueError:
            pass
        else:
            ips.add(node.hostname)

        if node.has_bundle('network'):
            for network in node.metadata.get('network').values():
                if 'ipv4' in network:
                    ips.add(str(ip_interface(network['ipv4']).ip))
                if 'ipv6' in network:
                    ips.add(str(ip_interface(network['ipv6']).ip))

        if node.has_bundle('wireguard'):
            ips.add(str(ip_interface(node.metadata.get('wireguard/my_ip')).ip))

    return ips
