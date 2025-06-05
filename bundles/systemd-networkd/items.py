assert node.has_bundle('systemd')

files = {
    '/etc/resolv.conf': {
        'content_type': 'mako',
    },
    '/etc/dhcp/dhclient-enter-hooks.d/nodnsupdate': {
        'mode': '0755',
    },
}

directories = {
    '/etc/systemd/network': {
        'purge': True,
    },
}

svc_systemd = {
    'systemd-networkd.service': {},
}
