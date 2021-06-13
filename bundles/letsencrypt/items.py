assert node.has_bundle('nginx')

directories = {
    '/etc/dehydrated/conf.d': {},
    '/var/lib/dehydrated/acme-challenges': {},
}

files = {
    '/etc/dehydrated/domains.txt': {
        'content_type': 'mako',
        'triggers': {
            'action:letsencrypt_update_certificates',
        },
    },
    '/etc/dehydrated/config': {
        'triggers': {
            'action:letsencrypt_update_certificates',
        },
    },
    '/etc/dehydrated/hook.sh': {
        'content_type': 'mako',
        'mode': '0755',
    },
    '/etc/dehydrated/letsencrypt-ensure-some-certificate': {
        'mode': '0755',
    },
}

actions['letsencrypt_update_certificates'] = {
    'command': 'dehydrated --cron --accept-terms --challenge http-01',
    'triggered': True,
    'needs': {
        'svc_systemd:nginx',
    },
}

for domain, _ in node.metadata.get('letsencrypt/domains').items():
    actions['letsencrypt_ensure-some-certificate_{}'.format(domain)] = {
        'command': '/etc/dehydrated/letsencrypt-ensure-some-certificate {}'.format(domain),
        'unless': '/etc/dehydrated/letsencrypt-ensure-some-certificate {} true'.format(domain),
        'needs': {
            'file:/etc/dehydrated/letsencrypt-ensure-some-certificate',
        },
        'needed_by': {
            'svc_systemd:nginx',
        },
        'triggers': {
            'action:letsencrypt_update_certificates',
        },
    }
