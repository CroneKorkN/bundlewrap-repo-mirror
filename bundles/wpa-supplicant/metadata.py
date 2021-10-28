import hashlib, binascii


defaults = {
    'apt': {
        'packages': {
            'wpasupplicant': {},
        },
    },
}

@metadata_reactor.provides(
    'wpa-supplicant/psk',
)
def psk(metadata):
    return {
        'wpa-supplicant': {
            'psk': binascii.hexlify(
                hashlib.pbkdf2_hmac(
                    'sha1',
                    repo.vault.decrypt(metadata.get('wpa-supplicant/password')).value.encode(),
                    metadata.get('wpa-supplicant/ssid').encode(),
                    4096,
                    32
                )
            ).decode()
        }
    }
    
