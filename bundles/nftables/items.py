files = {
    '/etc/nftables.conf': {
        'content_type': 'mako',
        'mode': '0755',
        'context': {
            'input': node.metadata.get('nftables/input'),
            'forward': node.metadata.get('nftables/forward'),
            'output': node.metadata.get('nftables/output'),
        },
        'triggers': [
            'svc_systemd:nftables.service:reload',
        ],
    },
}

svc_systemd = {
    'nftables.service': {
        'needs': [
            'pkg_apt:nftables',
        ],
    },
}
