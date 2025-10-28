from bundlewrap.utils.dicts import merge_dict

files = {}
svc_systemd = {}

directories = {
    '/usr/local/lib/systemd/system': {
        'purge': True,
        'triggers': [
            "action:systemd-reload",
        ],
    },
}

actions = {
     'systemd-reload': {
        'command': 'systemctl daemon-reload',
        'cascade_skip': False,
        'triggered': True,
    },
}

for name, unit in node.metadata.get('systemd/units').items():
    extension = name.split('.')[1]

    if extension in ['netdev', 'network']:
        path = f'/etc/systemd/network/{name}'
        dependencies = {
            'needed_by': [
                'svc_systemd:systemd-networkd.service',
            ],
            'triggers': [
                'svc_systemd:systemd-networkd.service:restart',
            ],
        }
    elif extension in ['timer', 'service', 'mount', 'swap', 'target']:
        path = f'/usr/local/lib/systemd/system/{name}'
        dependencies = {
            'triggers': [
                "action:systemd-reload",
            ],
        }
        if name in node.metadata.get('systemd/services'):
            dependencies['triggers'].append(f'svc_systemd:{name}:restart')
    else:
        raise Exception(f'unknown type {extension}')

    for attribute in ['needs', 'needed_by', 'triggers', 'triggered_by']:
        if attribute in unit:
            dependencies[attribute] = unit.pop(attribute)

    files[path] = {
        'content': repo.libs.systemd.generate_unitfile(unit),
        **dependencies,
    }

for name, config in node.metadata.get('systemd/services').items():
    svc_systemd[name] = merge_dict(config, {
        'needs': [
            'action:systemd-reload',
        ],
    })

files['/etc/systemd/logind.conf'] = {
    'content': repo.libs.systemd.generate_unitfile({
        'Login': node.metadata.get('systemd/logind'),
    }),
}
