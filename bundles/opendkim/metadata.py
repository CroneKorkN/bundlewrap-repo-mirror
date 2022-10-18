from re import sub
from cryptography.hazmat.primitives import serialization as crypto_serialization
from base64 import b64decode


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
        privkey = repo.libs.rsa.generate_deterministic_rsa_private_key(
            repo.path,
            b64decode(str(repo.vault.random_bytes_as_base64_for('dkim' + domain)))
        )
        keys[domain] = {
            'private': privkey.private_bytes(
                crypto_serialization.Encoding.PEM,
                crypto_serialization.PrivateFormat.PKCS8,
                crypto_serialization.NoEncryption()
            ).decode(),
            'public': ''.join(
                privkey.public_key().public_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PublicFormat.SubjectPublicKeyInfo
                ).decode().split('\n')[1:-2]
            ),
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
