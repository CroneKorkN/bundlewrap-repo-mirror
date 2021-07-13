timezone = node.metadata.get('timezone', 'UTC')
keymap = node.metadata.get('keymap', 'de')

actions = {
     'systemd-reload': {
        'command': 'systemctl daemon-reload',
        'cascade_skip': False,
        'triggered': True,
    }, 
}

for name, config in node.metadata.get('systemd/units').items():
    files[config['path']] = {
        'content': repo.libs.systemd.generate_unitfile(config['content']),
        **config['item'],
    }
    files[config['path']].setdefault('triggers', []).append("action:systemd-reload")

for name, config in node.metadata.get('systemd/services').items():
    svc_systemd[name] = {
        **config,
    }
    svc_systemd[name].setdefault('needs', []).append("action:systemd-reload")
