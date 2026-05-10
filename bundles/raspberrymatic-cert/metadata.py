defaults = {
    'systemd-timers': {
        'raspberrymatic-cert': {
            'command': '/opt/raspberrymatic-cert',
            'when': 'daily',
        },
    },
}


@metadata_reactor.provides(
    'letsencrypt/domains',
)
def letsencrypt(metadata):
    return {
        'letsencrypt': {
            'domains': {
                metadata.get('raspberrymatic-cert/domain'): {
                    'start': ['raspberrymatic-cert'],
                },
            },
        },
    }
