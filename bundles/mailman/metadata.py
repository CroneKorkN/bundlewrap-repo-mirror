defaults = {
    'apt': {
        'packages': {
            'mailman3-full': {},
            'postfix': {},
            'apache2': {
                'installed': False,
                'needs': {
                    'pkg_apt:mailman3-full',
                },
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/mailman': {
                'mountpoint': '/var/lib/mailman3',
            },
        },
    },
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('mailman/hostname'): {
                    'content': 'mailman/vhost.conf',
                },
            },
        },
    }
