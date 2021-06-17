from ipaddress import ip_interface

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
    'dns',
)
def dns(metadata):
    dns = {}
    
    for config in metadata.get('nginx/vhosts', {}).values():
        dns[config['domain']] = {}
        
        if metadata.get('network/ipv4'):
            dns[config['domain']]['A'] = [
                str(ip_interface(metadata.get('network/ipv4')).ip)
            ]
        if metadata.get('network/ipv6'):
            dns[config['domain']]['AAAA'] = [
                str(ip_interface(metadata.get('network/ipv6')).ip)
            ]

    return {
        'dns': dns,
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
