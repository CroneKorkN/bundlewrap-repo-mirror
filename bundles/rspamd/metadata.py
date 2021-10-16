from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'clamav': {},
            'clamav-daemon': {},
            'clamav-freshclam': {},
            'clamav-unofficial-sigs': {}, 
            'rspamd': {},
        },
    },
    'nginx': {
        'vhosts': {
            'rspamd.sublimity.de': {
                'content': 'nginx/proxy_pass.conf',
                'context': {
                    'target': 'http://localhost:11334',
                },
            },
        },
    },
    'rspamd': {
        'web_password': repo.vault.password_for(node.name + ' rspamd web password'),
        'ip_whitelist': [],
    },
}


@metadata_reactor.provides(
    'rspamd/ip_whitelist',
)
def ignored_ips(metadata):
    return {
        'rspamd': {
            'ip_whitelist': {
                str(ip_interface(network['ipv4']).ip)
                    for other_node in repo.nodes
                    for network in other_node.metadata.get('network').values()
            }
        },
    }
