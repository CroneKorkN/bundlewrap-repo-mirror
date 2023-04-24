from ipaddress import ip_interface

files = {
    '/opt/zfs-mirror': {
        'mode': '550',
        'content_type': 'mako',
        'context': {
            'server_ip': ip_interface(
                repo.get_node(node.metadata.get('zfs-mirror/server')).metadata.get('network/internal_ipv4')
            ).ip,
        },
    }
}
