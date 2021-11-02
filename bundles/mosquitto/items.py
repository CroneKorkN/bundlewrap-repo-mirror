directories = {
    '/etc/mosquitto': {},
    '/etc/mosquitto/conf.d': {
        'purge': True,
    },
}

files = {
    '/etc/mosquitto/conf.d/managed.conf': {
        'content_type': 'mako',
        'context': {
            'hostname': node.metadata.get('mosquitto/hostname'),
        },
        'needs': [
            'pkg_apt:mosquitto',
        ],
        'needed_by': [
            'svc_systemd:mosquitto'
        ],
        'triggers': [
            'svc_systemd:mosquitto:restart'
        ],
    },
}

svc_systemd = {
    'mosquitto': {
        'needs': [
            'pkg_apt:mosquitto',
            'action:moquitto-generate-dhparam',
        ],
    },
}

actions = {
    'moquitto-generate-dhparam': {
        'command': 'openssl dhparam -out /etc/mosquitto/dhparam.pem 2048',
        'unless': 'test -f /etc/mosquitto/dhparam.pem',
        'needs': [
            'pkg_apt:mosquitto',
        ],
        'triggers': [
            'svc_systemd:mosquitto:restart'
        ],
    },
}
