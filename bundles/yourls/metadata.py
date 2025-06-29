defaults = {
    'mariadb': {
        'databases': {
            'yourls': {
                'password': repo.vault.random_bytes_as_base64_for(f'{node.name} yourls DB', length=32).value,
            },
        },
    },
}


@metadata_reactor.provides(
    'apt/packages',
)
def apt(metadata):
    php_version = metadata.get('php/version')

    return {
        'apt':{
            'packages': {
                f'php{php_version}-mysql': {},
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
                metadata.get('yourls/hostname'): {
                    'content': 'yourls/vhost.conf',
                    'context': {
                        'php_version': metadata.get('php/version'),
                    },
                    'check_path': '/admin',
                },
            },
        },
    }
