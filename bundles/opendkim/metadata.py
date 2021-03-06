from os.path import join, exists
from re import sub
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
        'keys': {},
    },
}


@metadata_reactor.provides(
    'opendkim/keys',
)
def keys(metadata):
    keys = {}
    
    for domain in metadata.get('mailserver/domains'):
        if domain in metadata.get(f'opendkim/keys'):
            continue
        
        pubkey_path = join(repo.path, 'data', 'dkim', f'{domain}.pubkey')
        privkey_path = join(repo.path, 'data', 'dkim', f'{domain}.privkey.enc')
        
        if not exists(pubkey_path) or not exists(privkey_path):
            key = rsa.generate_private_key(
                backend=crypto_default_backend(),
                public_exponent=65537,
                key_size=2048
            )
            with open(pubkey_path, 'w') as file:
                file.write(
                    ''.join(
                        key.public_key().public_bytes(
                            crypto_serialization.Encoding.PEM,
                            crypto_serialization.PublicFormat.SubjectPublicKeyInfo
                        ).decode().split('\n')[1:-2]
                    )
                )
            with open(privkey_path, 'w') as file:
                file.write(
                    repo.vault.encrypt(
                        key.private_bytes(
                            crypto_serialization.Encoding.PEM,
                            crypto_serialization.PrivateFormat.PKCS8,
                            crypto_serialization.NoEncryption()
                        ).decode()
                    )
                )
                
        with open(pubkey_path, 'r') as pubkey:
            with open(privkey_path, 'r') as privkey:
                keys[domain] = {
                    'public': pubkey.read(),
                    'private': repo.vault.decrypt(privkey.read()),
                }

    return {
        'opendkim': {
            'keys': keys,
        }
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    dns = {}
    
    for domain, keys in metadata.get('opendkim/keys').items():
        raw_key = sub('^ssh-rsa ', '', keys['public'])
        dns[f'mail._domainkey.{domain}'] = {
            'TXT': [f'v=DKIM1; k=rsa; p={raw_key}'],
        }
    
    return {
        'dns': dns,
    }
