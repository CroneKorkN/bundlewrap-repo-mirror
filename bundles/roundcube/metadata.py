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
            'php-net-idna2': {},
            'php-net-smtp': {},
            'php-net-socket': {},
            'php-pear': {},
            'php-pgsql': {},
            'php-xml': {},
            'php-zip': {},
        },
    },
    'nginx': {
        'vhosts': {
            'roundcube': {
                'webroot': '/opt/roundcube',
                'php': True,
            },
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
        'des_key': repo.vault.password_for(f'{node.name} roundcube des_key'),
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
}

@metadata_reactor.provides(
    'nginx/vhosts/roundcube/domain'
)
def domain(metadata):
    return {
        'nginx': {
            'vhosts': {
                'roundcube': {
                    'domain': metadata.get('mailserver/hostname'),
                },
            },
        },
    }
