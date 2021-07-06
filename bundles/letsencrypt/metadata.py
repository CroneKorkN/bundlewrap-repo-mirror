defaults = {
    'apt': {
        'packages': {
            'dehydrated': {},
        },
    },
    'cron': {
        'letsencrypt_renew': '{} 4 * * *    root    /usr/bin/dehydrated --cron --accept-terms --challenge http-01 > /dev/null'.format((node.magic_number % 60)),
        'letsencrypt_cleanup': '{} 4 * * 0    root    /usr/bin/dehydrated --cleanup > /dev/null'.format((node.magic_number % 60)),
    },
    'letsencrypt': {
        'domains': {},
    },
    'pacman': {
        'packages': {
            'dehydrated': {},
        },
    },
}


@metadata_reactor.provides(
    'letsencrypt/domains'
)
def delegated_domains(metadata):
    return {
        'letsencrypt': {
            'domains': {
                domain: {}
                    for other_node in repo.nodes
                    if other_node.has_bundle('letsencrypt')
                        and other_node.metadata.get('letsencrypt/delegate_to_node', None) == node.name
                    for domain in other_node.metadata.get('letsencrypt/domains').keys()
            },
        },
    }
