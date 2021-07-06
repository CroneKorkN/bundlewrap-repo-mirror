from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'nginx': {},
        },
    },
    'nginx': {
        'default_vhosts': {
            '80': {
                'listen': [
                    '80',
                    '[::]:80',
                ],
                'location /.well-known/acme-challenge/': {
                    'alias': '/var/lib/dehydrated/acme-challenges/',
                },
                'location /': {
                    'return': '301 https://$host$request_uri',
                },
            },
            'stub_status': {
               'listen': '127.0.0.1:22999 default_server',
               'server_name': '_',
               'stub_status': '',
            },
        },
        'vhosts': {
            # '80': {
            #     'content': 'nginx/80.conf',
            # },
            # 'stub_status': {
            #     'content': 'nginx/stub_status.conf',
            # },
        },
        'includes': {},
    },
}

@metadata_reactor.provides(
    'nginx/includes',
)
def includes(metadata):
    return {
        'nginx': {
            'includes': {
                'php': {
                    'location ~ \.php$': {
                        'include': 'fastcgi.conf',
                        'fastcgi_split_path_info': '^(.+\.php)(/.+)$',
                        'fastcgi_pass': f"unix:/run/php/php{metadata.get('php/version')}-fpm.sock",
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
            domain: repo.libs.dns.get_a_records(metadata)
                for domain in metadata.get('nginx/vhosts')
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
