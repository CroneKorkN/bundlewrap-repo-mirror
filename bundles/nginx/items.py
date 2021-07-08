from datetime import datetime, timedelta
from mako.template import Template
from os.path import join

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
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }, 
    '/etc/nginx/fastcgi.conf': {
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }, 
    '/etc/nginx/sites/80.conf': {
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }, 
    '/etc/nginx/sites/stub_status.conf': {
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }, 
    '/etc/nginx/sites-available': {
        'delete': True,
    },
    '/etc/nginx/sites-enabled': {
        'delete': True,
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


for name, config in node.metadata.get('nginx/vhosts').items():
    files[f'/etc/nginx/sites/{name}'] = {
        'content': Template(filename=join(repo.path, 'data', config['content'])).render(
            server_name=name,
            **config.get('context', {}),
        ),
        'needs': [],
        'needed_by': {
            'svc_systemd:nginx',
            'svc_systemd:nginx:restart',
        },
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }
    
    if name in node.metadata.get('letsencrypt/domains'):
        files[f'/etc/nginx/sites/{name}']['needs'].append(
            f'action:letsencrypt_ensure-some-certificate_{name}',
        )
