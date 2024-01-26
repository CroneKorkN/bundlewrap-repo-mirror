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


@metadata_reactor.provides(
    'systemd-timers/raspberrymatic-cert',
)
def systemd_timers(metadata):
    return {
        'systemd-timers': {
            'raspberrymatic-cert': {
                'command': '/opt/raspberrymatic-cert',
                'when': 'daily',
            }
        },
    }
