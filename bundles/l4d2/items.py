directories = {
    '/etc/left4dead2': {
        'owner': 'steam',
        'purge': True,
    }
}

for name, config in node.metadata.get('left4dead2').items():
    config.pop('port')
    config['hostname'] = name
    
    files[f'/etc/left4dead2/{name}.cfg'] = {
        'content': '\n'.join(
            f'{key} "{value}"' for key, value in config.items()
        ),
        'owner': 'steam',
        'triggers': [
            f'svc_systemd:left4dead2-server-{name}:restart',
        ],
    }
    svc_systemd[f'left4dead2-server-{name}'] = {}
