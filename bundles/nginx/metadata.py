from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'nginx': {},
        },
    },
    'nginx': {
        'vhosts': {},
    },
}


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            domain: repo.libs.dns.get_a_records(metadata, internal=config.get('internal_dns', True))
                for domain, config in metadata.get('nginx/vhosts').items()
        },
    }


@metadata_reactor.provides(
    'letsencrypt/domains',
    'letsencrypt/reload_after',
)
def letsencrypt(metadata):
    return {
        'letsencrypt': {
            'domains': {
                domain: {} for domain in metadata.get('nginx/vhosts')
            },
            'reload_after': {
                'nginx',
            },
        },
    }
