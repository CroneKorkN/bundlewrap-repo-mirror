from shlex import quote


defaults = {
    'apt': {
        'packages': {
            'nginx': {},
            'apache2': {
                'installed': False,
            },
        },
    },
    'nftables': {
        'input': {
            'tcp dport {80, 443} accept',
        },
    },
    'nginx': {
        'vhosts': {},
        'modules': set(),
    },
    'systemd': {
        'units': {
            'nginx.service.d/override.conf': {
                'Unit': {
                    'After': {'network-online.target'},
                    'Wants': {'network-online.target'},
                },
            },
        },
    },
}


@metadata_reactor.provides(
    'nginx/vhosts',
)
def vhosts(metadata):
    vhosts = {}

    for name, config in metadata.get('nginx/vhosts').items():
        vhosts[name] = {
            'server_name': name,
            'listen': [
                '443 ssl http2',
                '[::]:443 ssl http2',
            ],
            'ssl_certificate': f'/var/lib/dehydrated/certs/{name}/fullchain.pem',
            'ssl_certificate_key': f'/var/lib/dehydrated/certs/{name}/privkey.pem',
            'location /.well-known/acme-challenge/': {
                'alias': '/var/lib/dehydrated/acme-challenges/',
            },
        }

    return {
        'nginx': {
            'vhosts': vhosts,
        }
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            domain: repo.libs.ip.get_a_records(metadata, internal=config.get('internal_dns', True))
                for domain, config in metadata.get('nginx/vhosts').items()
        },
    }


@metadata_reactor.provides(
    'letsencrypt/domains',
)
def letsencrypt(metadata):
    return {
        'letsencrypt': {
            'domains': {
                domain: {
                    'reload': {'nginx'},
                }
                    for domain in metadata.get('nginx/vhosts').keys()
            },
        },
    }


@metadata_reactor.provides(
    'monitoring/services',
)
def monitoring(metadata):
    return {
        'monitoring': {
            'services': {
                hostname: {
                    'vars.command': f"/usr/bin/curl -X GET -L --fail --no-progress-meter -o /dev/null {quote(hostname + vhost.get('check_path', ''))}",
                }
                    for hostname, vhost in metadata.get('nginx/vhosts').items()
            },
        },
    }


@metadata_reactor.provides(
    'apt/packages',
)
def modules(metadata):
    return {
        'apt': {
            'packages': {
                f'libnginx-mod-{module}': {}
                    for module in metadata.get('nginx/modules')
            },
        },
    }
