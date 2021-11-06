assert node.has_bundle('nginx')

from ipaddress import ip_interface

delegated = 'delegate_to_node' in node.metadata.get('letsencrypt')
acme_node = repo.get_node(node.metadata.get('letsencrypt/acme_node'))

directories = {
    '/etc/dehydrated/conf.d': {},
    '/var/lib/dehydrated/acme-challenges': {},
}

files = {
    '/etc/dehydrated/domains.txt': {
        'content_type': 'mako',
        'context': {
            'domains': node.metadata.get('letsencrypt/domains'),
        },
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
            'server': ip_interface(acme_node.metadata.get('network/external/ipv4')).ip,
            'zone': acme_node.metadata.get('bind/acme_zone'),
            'acme_key': acme_node.metadata.get('bind/keys/' + acme_node.metadata.get('bind/acme_zone')),
            'domains': node.metadata.get('letsencrypt/domains'),
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
    'command': 'true || dehydrated --cron --accept-terms --challenge http-01',
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
