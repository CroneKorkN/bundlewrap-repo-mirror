from hashlib import sha3_256

defaults = {
    'apt': {
        'packages': {
            'icinga2': {},
            'icingaweb2': {},
            'icinga2-ido-pgsql': {},
            'icingacli': {},
            'monitoring-plugins': {},
        },
        'sources': {
            'deb https://packages.icinga.com/debian icinga-{release} main',
        },
    },
    'postgresql': {
        'databases': {
            'icinga2': {
                'owner': 'icinga2',
            },
            'icingaweb2': {
                'owner': 'icingaweb2',
            },
        },
        'roles': {
            'icinga2': {
                'password': repo.vault.password_for(f'psql icinga2 on {node.name}'),
            },
            'icingaweb2': {
                'password': repo.vault.password_for(f'psql icingaweb2 on {node.name}'),
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/icinga2': {
                'mountpoint': '/var/lib/icinga2',
                'needed_by': {
                    'pkg_apt:icinga2',
                    'pkg_apt:icingaweb2',
                    'pkg_apt:icinga2-ido-pgsql',
                },
            },
        },
    },
}


@metadata_reactor.provides(
    'icingaweb2/setup_token',
)
def setup_token(metadata):
    return {
        'icingaweb2': {
            'setup_token': sha3_256(metadata.get('id').encode()).hexdigest()[:16],
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('icinga2/hostname'): {
                    'content': 'icingaweb2/vhost.conf',
                    'context': {
                    },
                },
            },
        },
    }
