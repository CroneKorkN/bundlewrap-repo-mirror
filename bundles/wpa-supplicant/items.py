import hashlib, binascii


def wpa_psk(ssid, password):
    return binascii.hexlify(
        hashlib.pbkdf2_hmac('sha1', str.encode(password), str.encode(ssid), 4096, 32)
    ).decode()
    

interface = node.metadata.get('wpa-supplicant/interface')
ssid = node.metadata.get('wpa-supplicant/ssid')
passowrd = repo.vault.decrypt(node.metadata.get('wpa-supplicant/password')).value
psk = wpa_psk(ssid, passowrd)

files = {
    f'/etc/wpa_supplicant/wpa_supplicant-{interface}.conf': {
        'source': 'wpa_supplicant.conf',
        'content_type': 'mako',
        'context': {
            'ssid': ssid,
            'psk': psk,
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
