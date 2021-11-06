assert node.has_bundle('nginx')

delegated = 'delegate_to_node' in node.metadata.get('letsencrypt')

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
        'context': {
            'server': node.metadata.get('network/external/ipv4').split('/')[0],
            'zone': node.metadata.get('bind/acme_hostname'),
            'acme_key': node.metadata.get('bind/keys/acme'),
        },
        'mode': '0755',
    },
    '/etc/dehydrated/letsencrypt-ensure-some-certificate': {
        'mode': '0755',
    },
    '/etc/dehydrated/letsencrypt-ensure-some-certificate': {
        'mode': '0755',
    },
}

actions['letsencrypt_update_certificates'] = {
    'command': 'dehydrated --cron --accept-terms --challenge http-01',
    'triggered': True,
    'skip': delegated,
    'needs': {
        'svc_systemd:nginx',
    },
}

for domain in node.metadata.get('letsencrypt/domains').keys():
    actions[f'letsencrypt_ensure-some-certificate_{domain}'] = {
        'command': f'/etc/dehydrated/letsencrypt-ensure-some-certificate {domain}',
        'unless': f'/etc/dehydrated/letsencrypt-ensure-some-certificate {domain} true',
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
