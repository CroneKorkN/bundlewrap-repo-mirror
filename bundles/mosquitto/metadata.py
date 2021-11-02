defaults = {
    'apt': {
        'packages': {
            'mosquitto': {},
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
                metadata.get('mosquitto/hostname'): set(),
            },
        },
    }
