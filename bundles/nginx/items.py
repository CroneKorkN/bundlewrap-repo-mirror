from datetime import datetime, timedelta

directories = {
    '/etc/nginx/sites': {
        'purge': True,
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    },
    '/etc/nginx/ssl': {
        'purge': True,
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    },
    '/var/www': {},
}

files = {
     '/etc/nginx/nginx.conf': {
        'content_type': 'mako',
        'context': {
            'username': 'www-data',
            **node.metadata['nginx'],
        },
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }, 
    '/etc/nginx/sites/stub_status': {
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    },
    '/etc/nginx/sites/000-port80.conf': {
        'source': 'port80.conf',
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    },
}

actions = {
    'nginx-generate-dhparam': {
        'command': 'openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048',
        'unless': 'test -f /etc/ssl/certs/dhparam.pem',
    },
}

svc_systemd = {
    'nginx': {
        'needs': {
            'action:nginx-generate-dhparam',
            'pkg_apt:nginx',
        },
    },
}

for vhost, config in node.metadata.get('nginx/vhosts', {}).items():
    files[f'/etc/nginx/sites/{vhost}'] = {
        'source': 'site_template',
        'content_type': 'mako',
        'context': {
            'create_access_log': config.get('access_log', node.metadata.get('nginx/access_log', False)),
            'php_version': node.metadata.get('php/version', ''),
            'vhost': vhost,
            **config,
        },
        'needs': set(),
        'needed_by': {
            'svc_systemd:nginx',
            'svc_systemd:nginx:restart',
        },
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }

    if not 'webroot' in config:
        directories[f'/var/www/{vhost}'] = {}

        if node.has_bundle('zfs'):
            directories[f'/var/www/{vhost}']['needs'] = {
                'bundle:zfs',
            }

        directories[f'/var/www/{vhost}'].update(config.get('webroot_config', {}))

    if config.get('ssl', 'letsencrypt') == 'letsencrypt':
        files[f'/etc/nginx/sites/{vhost}']['needs'].add('action:letsencrypt_ensure-some-certificate_{}'.format(config['domain']))
        files[f'/etc/nginx/sites/{vhost}']['needed_by'].add('action:letsencrypt_update_certificates')

    elif config.get('ssl', 'letsencrypt'):
        files[f'/etc/nginx/ssl/{vhost}.crt'] = {
            'content_type': 'mako',
            'source': 'ssl_template',
            'context': {
                'domain': config['ssl'],
            },
            'needed_by': {
                'svc_systemd:nginx',
                'svc_systemd:nginx:restart',
            },
            'triggers': {
                'svc_systemd:nginx:reload',
            },
        }
        files[f'/etc/nginx/ssl/{vhost}.key'] = {
            'content': repo.vault.decrypt_file('ssl/{}.key.pem.vault'.format(config['ssl'])),
            'mode': '0600',
            'needed_by': {
                'svc_systemd:nginx',
                'svc_systemd:nginx:restart',
            },
            'triggers': {
                'svc_systemd:nginx:reload',
            },
        }

        files[f'/etc/nginx/sites/{vhost}']['needs'].add(f'file:/etc/nginx/ssl/{vhost}.crt')
        files[f'/etc/nginx/sites/{vhost}']['needs'].add(f'file:/etc/nginx/ssl/{vhost}.key')
