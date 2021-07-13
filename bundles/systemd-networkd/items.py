assert node.has_bundle('systemd')

files = {
    '/etc/network/interfaces': {
        'delete': True,
    },
    '/etc/resolv.conf': {
        'content_type': 'mako',
    },
}

directories = {
    '/etc/systemd/network': {
        'purge': True,
    },
}

svc_systemd = {
    'systemd-networkd': {},
}
