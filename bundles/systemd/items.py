from bundlewrap.utils.dicts import merge_dict

actions = {
     'systemd-reload': {
        'command': 'systemctl daemon-reload',
        'cascade_skip': False,
        'triggered': True,
    }, 
}

for name, unit in node.metadata.get('systemd/units').items():
    extension = name.split('.')[-1]

    if extension in ['netdev', 'network']:
        files[f'/etc/systemd/network/{name}'] = {
            'content': repo.libs.systemd.generate_unitfile(unit),
            'triggers': [
                'svc_systemd:systemd-networkd:restart',
            ],
        }
    elif extension in ['timer', 'service']:
        files[f'/etc/systemd/system/{name}'] = {
            'content': repo.libs.systemd.generate_unitfile(unit),
            'triggers': [
                "action:systemd-reload",
            ],
        }
    else:
        raise Exception(f'unknown unit extension: "{extension}"')

for name, config in node.metadata.get('systemd/services').items():
    svc_systemd[name] = merge_dict(config, {
        'needs': [
            'action:systemd-reload',
        ],
    })
