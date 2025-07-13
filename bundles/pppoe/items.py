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
    '/etc/dhcpcd.conf': {
        'content_type': 'mako',
    },
    '/etc/dhcpcd.exit-hook': {
        'mode': '0755',
    },
    '/etc/radvd.conf.template': {
        'content_type': 'mako',
    },
}

actions = {
    'touch_radvd.conf': {
        'command': 'touch /etc/radvd.conf',
        'unless': 'ls /etc/radvd.conf',
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
    'dhcpcd.service': {
        'needs': {
            'pkg_apt:dhcpcd5',
            'file:/etc/dhcpcd.conf',
            'file:/etc/dhcpcd.exit-hook',
            'action:touch_radvd.conf',
        },
    },
    'radvd.service': {
        'needs': {
            'pkg_apt:radvd',
        },
    },
}
