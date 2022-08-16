from hashlib import sha3_256

defaults = {
    'apt': {
        'packages': {
            'icingaweb2': {},
            'php-ldap': {},
            'php-json': {},
            'php-intl': {},
            'php-xml': {},
            'php-gd': {},
            'php-imagick': {},
            'php-pgsql': {},
        },
        'sources': {
            'deb https://packages.icinga.com/debian icinga-{release} main',
            'deb https://packages.icinga.com/debian icinga-{release}-snapshots main',
        },
    },
    'icingaweb2': {
        'authentication.ini': {
            'icingaweb2': {
                'backend': 'db',
                'resource': 'icingaweb2_db',
            },
        },
        'config.ini': {
            'global': {
                'show_stacktraces': '1',
                'show_application_state_messages': '1',
                #'module_path': '/usr/share/icingaweb2/modules',
                'config_backend': 'db',
                'config_resource': 'icingaweb2_db',
            },
            'logging': {
                'log': 'syslog',
                'level': 'INFO',
                'application': 'icingaweb2',
                'facility': 'user',
            },
        },
        'groups.ini': {
            'icingaweb2': {
                'backend': 'db',
                'resource': 'icingaweb2_db',
            },
        },
        'resources.ini': {
            'icingaweb2_db': {
                'type': 'db',
                'db': 'pgsql',
                'host': 'localhost',
                'port': '5432',
                'dbname': 'icingaweb2',
                'username': 'icingaweb2',
                'password': str(repo.vault.password_for(f'psql icingaweb2 on {node.name}')),
                'charset': '',
                'use_ssl': '0',
            },
        },
        'roles.ini': {
            'Administrators': {
                'users': 'root',
                'permissions': '*',
                'groups': 'Administrators',
            },
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
        'icingaweb2': {},
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
    'icingaweb2/root_password',
)
def setup_token(metadata):
    return {
        'icingaweb2': {
            'setup_token': sha3_256(metadata.get('id').encode()).hexdigest()[:16],
            'root_password': str(repo.vault.password_for(f"icingaweb2 root user on {metadata.get('id')}")),
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
