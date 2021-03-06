database_password = repo.vault.password_for(f'{node.name} postgresql roundcube')

defaults = {
    'apt': {
        'packages': {
            'php': {},
            'php-auth-sasl': {},
            'php-cli': {},
            'php-fpm': {},
            'php-imagick': {},
            'php-intl': {},
            'php-mail-mime': {},
            'php-mbstring': {},
            # FIXME: not available in bullseye?
            # 'php-net-idna2': {}, 
            'php-net-smtp': {},
            'php-net-socket': {},
            'php-pear': {},
            'php-pgsql': {},
            'php-xml': {},
            'php-zip': {},
            'php-curl': {},
            'php-gd': {},
            'composer': {},
            'php-ldap': {},
        },
    },
    'roundcube': {
        'database': {
            'provider': 'pgsql',
            'host': 'localhost',
            'name': 'roundcube',
            'user': 'roundcube',
            'password': database_password,
        },
        'plugins': [
            'managesieve',
            'password',
        ],
        'des_key': repo.vault.password_for(f'{node.name} roundcube des_key', length=24),
    },
    'postgresql': {
        'roles': {
            'roundcube': {
                'password': database_password,
            },
        },
        'databases': {
            'roundcube': {
                'owner': 'roundcube',
            },
        },
    },
    'sudoers': {
        'www-data': ['/usr/bin/doveadm pw -s ARGON2ID'],
    },
}

@metadata_reactor.provides(
    'nginx/vhosts'
)
def vhost(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('mailserver/hostname'): {
                    'content': 'roundcube/vhost.conf',
                    'context': {
                        'root': '/opt/roundcube',
                    },
                },
            },
        },
    }
