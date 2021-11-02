defaults = {
    'apt': {
        'packages': {
            'mosquitto': {},
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
