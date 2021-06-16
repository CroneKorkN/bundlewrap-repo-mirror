from os.path import join, exists
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


defaults = {
    'apt': {
        'packages': {
            'opendkim': {},
            'opendkim-tools': {},
        },
    },
    'opendkim': {
        'domains': [],
        'keys': {},
    },
}

@metadata_reactor.provides(
    'opendkim/keys'
)
def keys(metadata):
    keys = {}
    
    for domain in metadata.get('opendkim/domains'):
        if domain in metadata.get(f'opendkim/keys'):
            continue
        
        pubkey_path = join(repo.path, 'data', 'dkim', f'{domain}.privkey')
        privkey_path = join(repo.path, 'data', 'dkim', f'{domain}.pubkey')
        
        if not exists(pubkey_path) or not exists(privkey_path):
            key = rsa.generate_private_key(
                backend=crypto_default_backend(),
                public_exponent=65537,
                key_size=2048
            )
            with open(pubkey_path, 'w') as file:
                file.write(     
                    key.public_key().public_bytes(
                        crypto_serialization.Encoding.OpenSSH,
                        crypto_serialization.PublicFormat.OpenSSH
                    ).decode()
                )
            with open(privkey_path, 'w') as file:
                file.write(
                    key.private_bytes(
                        crypto_serialization.Encoding.PEM,
                        crypto_serialization.PrivateFormat.PKCS8,
                        crypto_serialization.NoEncryption()
                    ).decode()
                )
                
        with open(pubkey_path, 'r') as pubkey:
            with open(privkey_path, 'r') as privkey:
                keys[domain] = {
                    'public': pubkey.read(),
                    'private': privkey.read(),
                }

    return {
        'opendkim': {
            'keys': keys,
        }
    }
