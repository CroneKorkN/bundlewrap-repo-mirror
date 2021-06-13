from bundlewrap.metadata import atomic

defaults = {
    'apt': {
        'packages': {
            'nginx': {},
        },
    },
    'nginx': {
        'worker_connections': 768,
    },
}


@metadata_reactor.provides(
    'letsencrypt/domains',
    'letsencrypt/reload_after',
    'nginx/vhosts',
)
def letsencrypt(metadata):
    if not node.has_bundle('letsencrypt'):
        raise DoNotRunAgain

    domains = {}
    vhosts = {}

    for vhost, config in metadata.get('nginx/vhosts', {}).items():
        if config.get('ssl', 'letsencrypt') == 'letsencrypt':
            domain = config.get('domain', vhost)
            domains[domain] = config.get('domain_aliases', set())
            vhosts[vhost] = {
                'ssl': 'letsencrypt',
            }

    return {
        'letsencrypt': {
            'domains': domains,
            'reload_after': {
                'nginx',
            },
        },
        'nginx': {
            'vhosts': vhosts,
        },
    }
