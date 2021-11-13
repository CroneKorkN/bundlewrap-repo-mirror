defaults = {
    'php': {
        'post_max_size': '32G',
        'www.conf': {
            'user': 'www-data',
            'group': 'www-data',
            'listen': '/run/php/php7.4-fpm.sock',
            'listen.owner': 'www-data',
            'listen.group': 'www-data',
            'pm': 'dynamic',
            'pm.max_children': '5',
            'pm.start_servers': '2',
            'pm.min_spare_servers': '1',
            'pm.max_spare_servers': '3',
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
