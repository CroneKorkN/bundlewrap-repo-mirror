from ipaddress import ip_address, ip_interface


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
    'redis': {
        'rspamd': {},
    },
    'rspamd': {
        'web_password': repo.vault.password_for(node.name + ' rspamd web password'),
        'ip_whitelist': set(),
    },
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx_vhost(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('rspamd/hostname'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://localhost:11334',
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'rspamd/ip_whitelist',
)
def ignored_ips(metadata):
    return {
        'rspamd': {
            'ip_whitelist': repo.libs.ip.get_all_ips(repo.nodes),
        },
    }
