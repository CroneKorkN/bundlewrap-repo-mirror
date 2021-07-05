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
        'content': repo.libs.nginx.render_config(node.metadata.get('nginx/config')),
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }, 
    '/etc/nginx/fastcgi.conf': {
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

for name, config in node.metadata.get('nginx/includes').items():
    files[f'/etc/nginx/{name}.conf'] = {
        'content': repo.libs.nginx.render_config(config),
        'needed_by': {
            'svc_systemd:nginx',
            'svc_systemd:nginx:restart',
        },
        'triggers': {
            'svc_systemd:nginx:restart',
        },
    }
    
for name, config in {
    **node.metadata.get('nginx/default_vhosts'),
    **node.metadata.get('nginx/vhosts'),
}.items():
    files[f'/etc/nginx/sites/{name}'] = {
        'content': repo.libs.nginx.render_config({
            'server': config,
        }),
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
