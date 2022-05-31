defaults = {
    'php': {
        'post_max_size': '32G',
    },
}


@metadata_reactor.provides(
    'php/www.conf',
)
def www_conf(metadata):
    version = metadata.get('php/version')
    return {
        'php': {
            'www.conf': {
                'user': 'www-data',
                'group': 'www-data',
                'listen': f'/run/php/php{version}-fpm.sock',
                'listen.owner': 'www-data',
                'listen.group': 'www-data',
                'pm': 'dynamic',
                'pm.max_children': '30',
                'pm.start_servers': '10',
                'pm.min_spare_servers': '5',
                'pm.max_spare_servers': '10',
                'pm.max_requests': '500',
            },
        },
    }


@metadata_reactor.provides(
    'apt/packages',
)
def apt(metadata):
    version = metadata.get('php/version')
    return {
        'apt': {
            'packages': {
                f'php{version}': {},
                f'php{version}-fpm': {},
            },
        },
    }
