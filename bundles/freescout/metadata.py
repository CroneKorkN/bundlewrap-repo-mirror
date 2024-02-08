database_password = repo.vault.password_for(f'{node.name} postgresql freescout').value

defaults = {
    'apt': {
        'packages': {
            'php': {},
            'php-mysql': {},
            'php-fpm': {},
            'php-mbstring': {},
            'php-xml': {},
            'php-imap': {},
            'php-zip': {},
            'php-gd': {},
            'php-curl': {},
            'php-intl': {},
        },
    },
    'php': {
        'php.ini': {
            'cgi': {
                'fix_pathinfo': '0',
            },
        },
    },
    'postgresql': {
        'roles': {
            'freescout': {
                'password': database_password,
            },
        },
        'databases': {
            'freescout': {
                'owner': 'freescout',
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
                metadata.get('freescout/domain'): {
                    'content': 'freescout/vhost.conf',
                },
            },
        },
    }
