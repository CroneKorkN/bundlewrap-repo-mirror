from hashlib import sha3_256

defaults = {
    'apt': {
        'packages': {
            'icingaweb2': {},
        },
        'sources': {
            'deb https://packages.icinga.com/debian icinga-{release} main',
            'deb https://packages.icinga.com/debian icinga-{release}-snapshots main',
        },
    },
    'postgresql': {
        'databases': {
            'icingaweb2': {
                'owner': 'icingaweb2',
            },
        },
        'roles': {
            'icingaweb2': {
                'password': str(repo.vault.password_for(f'psql icingaweb2 on {node.name}')),
            },
        },
    },
    'redis': {
        'icingadb': {},
    },
}


@metadata_reactor.provides(
    'icingaweb2/hostname',
)
def hostname(metadata):
    return {
        'icingaweb2': {
            'hostname': metadata.get('icinga2/hostname'),
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
                metadata.get('icingaweb2/hostname'): {
                    'content': 'icingaweb2/vhost.conf',
                    'context': {
                    },
                },
            },
        },
    }
