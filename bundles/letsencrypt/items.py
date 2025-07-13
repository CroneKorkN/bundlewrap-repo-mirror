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
            'server': ip_interface(acme_node.metadata.get('network/internal/ipv4')).ip,
            'zone': acme_node.metadata.get('bind/acme_zone'),
            'acme_key_name': 'acme',
            'acme_key': acme_node.metadata.get('bind/views/external/keys/acme/token'),
            'domains': node.metadata.get('letsencrypt/domains'),
        },
        'mode': '0755',
    },
    '/etc/dehydrated/letsencrypt-ensure-some-certificate': {
        'mode': '0755',
    },
}

actions['letsencrypt_update_certificates'] = {
    'command': 'systemctl start letsencrypt.service',
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
            'pkg_apt:dehydrated',
        },
        'needed_by': {
            'svc_systemd:nginx',
        },
        'triggers': {
           'action:letsencrypt_update_certificates',
        },
    }

if node.has_bundle('dns'):
    actions['letsencrypt_update_certificates']['needs'].add('svc_systemd:named:restart')
