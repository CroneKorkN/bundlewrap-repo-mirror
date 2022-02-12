from bundlewrap.utils.dicts import merge_dict

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
            'triggers': [
                'svc_systemd:systemd-networkd:restart',
            ],
        }
    elif extension in ['timer', 'service', 'mount', 'swap']:
        path = f'/etc/systemd/system/{name}'
        dependencies = {
            'triggers': [
                "action:systemd-reload",
            ],
        }
        if name in node.metadata.get('systemd/services'):
            dependencies['triggers'].append(f'svc_systemd:{name}:restart')
    else:
        raise Exception(f'unknown type {extension}')


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
