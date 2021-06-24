assert node.has_bundle('systemd')

files = {
    '/etc/network/interfaces': {
        'delete': True,
    },
}

files['/etc/resolv.conf'] = {
    'content_type': 'mako',
}

directories = {
    '/etc/systemd/network': {
        'purge': True,
    },
}

for interface, config in node.metadata['interfaces'].items():
    files[f'/etc/systemd/network/{interface}.network'] = {
        'source': 'interface.network',
        'content_type': 'mako',
        'context': {
            'interface': interface,
            'config': config,
        },
        'needed_by': {
            'svc_systemd:systemd-networkd',
        },
        'triggers': {
            'svc_systemd:systemd-networkd:restart',
        },
    }

for type, path in {
    'networks': '/etc/systemd/network/{}.network',
    'netdevs': '/etc/systemd/network/{}.netdev',
}.items():
    for name, config in node.metadata.get(f'systemd-networkd/{type}').items():
        files[path.format(name)] = {
            'content': repo.libs.systemd.generate_unitfile(config),
            'needed_by': {
                'svc_systemd:systemd-networkd',
            },
            'triggers': {
                'svc_systemd:systemd-networkd:restart',
            },
        }

svc_systemd = {
    'systemd-networkd': {},
}
