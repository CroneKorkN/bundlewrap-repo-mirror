import hashlib, binascii


interface = node.metadata.get('wpa-supplicant/interface')

files = {
    f'/etc/wpa_supplicant/wpa_supplicant-{interface}.conf': {
        'source': 'wpa_supplicant.conf',
        'content_type': 'mako',
        'context': {
            'ssid': node.metadata.get('wpa-supplicant/ssid'),
            'psk': node.metadata.get('wpa-supplicant/psk'),
        },
        'needs': [
            'pkg_apt:wpasupplicant',
        ],
        'triggers': [
            f'svc_systemd:wpa_supplicant@{interface}:restart',
        ],
    },
}

svc_systemd = {
    'wpa_supplicant': {
        'needs': [
            'pkg_apt:wpasupplicant',
        ],
    },
    f'wpa_supplicant@{interface}': {
        'needs': [
            f'file:/etc/wpa_supplicant/wpa_supplicant-{interface}.conf',
        ],
    },
}
