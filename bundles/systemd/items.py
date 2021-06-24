timezone = node.metadata.get('timezone', 'UTC')
keymap = node.metadata.get('keymap', 'de')

actions = {
     'systemd-reload': {
        'command': 'systemctl daemon-reload',
        'cascade_skip': False,
        'triggered': True,
        'needed_by': {
            'svc_systemd:',
        },
    }, 
}

for name, service in node.metadata.get('systemd/services').items():
    # dont call a service 'service' explicitly
    if name.endswith('.service'):
        raise Exception(name)

    # split unit file content data from item data
    content_data = service.pop('content')

    # default WantedBy=multi-user.target
    content_data\
        .setdefault('Install', {})\
        .setdefault('WantedBy', {'multi-user.target'})

    # create unit file
    unit_path = f'/etc/systemd/system/{name}.service'
    files[unit_path] = {
        'content': repo.libs.systemd.generate_unitfile(content_data),
        'triggers': [
            'action:systemd-reload',
            f'svc_systemd:{name}:restart',
        ],
    }

    # service depends on unit file
    service\
        .setdefault('needs', [])\
        .append(f'file:{unit_path}')

    # service
    svc_systemd[name] = service
