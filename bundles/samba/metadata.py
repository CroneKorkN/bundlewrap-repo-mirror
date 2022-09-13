from importlib.metadata import metadata


defaults = {
    'apt': {
        'packages': {
            'samba': {},
        },
    },
    'nftables': {
        'input': {
            'tcp dport 445 accept',
        },
    },
    'samba': {
        'shares': {},
    },
    'zfs': {
        'datasets': {
            'tank/samba': {
                'mountpoint': '/var/lib/samba',
            },
        },
    },
}


@metadata_reactor.provides(
    'zfs/datasets',
)
def zfs(metadata):
    return {
        'zfs': {
            'datasets': {
                f'tank/samba/{name}': {
                    'mountpoint': f'/var/lib/samba/usershares/{name}',
                }
                    for name in metadata.get('samba/shares')
            },
        },
    }


@metadata_reactor.provides(
    'samba/shares',
)
def passwords(metadata):
    return {
        'samba': {
            'shares': {
                name: {
                    'password': repo.vault.password_for(f'samba {name}'),
                }
                    for name, conf in metadata.get('samba/shares').items()
                    if not conf.get('password', None)
            },
        },
    }


@metadata_reactor.provides(
    'users',
)
def users(metadata):
    return {
        'users': {
            name: {}
                for name in metadata.get('samba/shares')
        },
    }
