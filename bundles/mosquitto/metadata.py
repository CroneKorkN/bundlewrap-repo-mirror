from hashlib import pbkdf2_hmac
from base64 import b64encode, b64decode

defaults = {
    'apt': {
        'packages': {
            'mosquitto': {},
        },
    },
    'mosquitto': {
        'users': {},
    },
}


def password_file_entry(username, password, salt):
    hash = pbkdf2_hmac('sha512', password.encode(), b64decode(salt), 101)
    return f"{username}:$7$101${salt}${b64encode(hash).decode()}"


@metadata_reactor.provides(
    'mosquitto/users'
)
def passwords_and_salts(metadata):
    return  {
        'mosquitto': {
            'users': {
                username: {
                    'password': str(
                        repo.vault.random_bytes_as_base64_for(
                            f"{metadata.get('id')} mosquitto {username}",
                            key='encrypt',
                            length=24,
                        )
                    ),
                    'salt': str(
                        repo.vault.random_bytes_as_base64_for(
                            f"{metadata.get('id')} mosquitto {username}",
                            key='generate',
                            length=12,
                        )
                    )
                }
                    for username in metadata.get('mosquitto/users')
            },
        },
    }


@metadata_reactor.provides(
    'mosquitto/users'
)
def password_file(metadata):
    return  {
        'mosquitto': {
            'users': {
                username: {
                    'password_file': password_file_entry(username, conf['password'], conf['salt']),
                }
                    for username, conf in metadata.get('mosquitto/users').items()
            },
        },
    }


@metadata_reactor.provides(
    'systemd-mount'
)
def mount_certs(metadata):
    return  {
        'systemd-mount': {
            '/etc/mosquitto/certs': {
                'source': '/var/lib/dehydrated/certs/' + metadata.get('mosquitto/hostname'),
                'user': 'mosquitto',
            },
        },
    }


@metadata_reactor.provides(
    'letsencrypt/domains'
)
def letsencrypt(metadata):
    return  {
        'letsencrypt': {
            'domains': {
                metadata.get('mosquitto/hostname'): {},
            },
        },
    }
