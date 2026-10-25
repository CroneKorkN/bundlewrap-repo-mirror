files = {
    '/etc/ppp/peers/isp': {
        'content_type': 'mako',
        'mode': '0644',
        'context': {
            'interface': node.metadata.get('pppoe/interface'),
            'user': node.metadata.get('pppoe/user'),
        },
        'needs': {
            'pkg_apt:pppoe',
        },
        'triggers': {
            'svc_systemd:pppoe-isp.service:restart',
        },
    },
    '/etc/ppp/chap-secrets': {
        'content_type': 'mako',
        'mode': '0600',
        'context': {
            'user': node.metadata.get('pppoe/user'),
            'secret': node.metadata.get('pppoe/secret'),
        },
        'needs': {
            'pkg_apt:pppoe',
        },
        'triggers': {
            'svc_systemd:pppoe-isp.service:restart',
        },
    },
}

svc_systemd = {
    'pppoe-isp.service': {
        'needs': {
            'file:/etc/ppp/peers/isp',
            'file:/etc/ppp/chap-secrets',
            'file:/etc/systemd/network/ppp0.network',
        },
    },
}
