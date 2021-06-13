from ipaddress import ip_network

repo.libs.tools.require_bundle(node, 'systemd-networkd')

network = ip_network(node.metadata['wireguard']['my_ip'], strict=False)

files = {
    '/etc/systemd/network/wg0.netdev': {
        'content_type': 'mako',
        'context': {
            'network': f'{network.network_address}/{network.prefixlen}',
            **node.metadata['wireguard'],
        },
        'needs': {
            'pkg_apt:wireguard',
        },
        'triggers': {
            'svc_systemd:systemd-networkd:restart',
        },
    },
}
