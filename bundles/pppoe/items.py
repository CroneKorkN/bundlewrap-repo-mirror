files = {
    '/etc/modules-load.d/pppoe.conf': {
        'content': 'pppoe\npppox\nppp_generic',
        'mode': '0644',
    },
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
    },
}

svc_systemd = {
    'pppoe-isp.service': {
        'needs': {
            'file:/etc/ppp/peers/isp',
            'file:/etc/ppp/chap-secrets',
        },
    },
    'qdisc-ppp0.service': {
        'needs': {
            'svc_systemd:pppoe-isp.service',
        },
    },
}
