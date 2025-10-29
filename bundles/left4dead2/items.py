users = {
    'steam': {
        'home': '/opt/l4d2/steam',
        'shell': '/bin/bash',
    },
}

directories = {
    '/opt/l4d2': {
        'owner': 'steam',
        'group': 'steam',
    },
    '/opt/l4d2/configs': {
        'owner': 'steam',
    },
}

files = {
    '/opt/l4d2/setup': {
        'mode': '755',
        'triggers': {
            'svc_systemd:left4dead2-initialize.service:restart',
        },
    },
    '/opt/l4d2/start': {
        'mode': '755',
        'triggers': {
            f'svc_systemd:left4dead2-{server_name}.service:restart'
                for server_name in node.metadata.get('left4dead2').keys()
        },
    },
}

svc_systemd = {
    'left4dead2-initialize.service': {
        'enabled': True,
        'running': None,
        'needs': {
            'file:/opt/l4d2/setup',
            'file:/usr/local/lib/systemd/system/left4dead2-initialize.service',
        },
    },
}

for server_name, config in node.metadata.get('left4dead2').items():
    files[f'/opt/l4d2/configs/{server_name}.cfg'] = {
        'content': '\n'.join(config.get('config', [])) + '\n',
        'owner': 'steam',
        'mode': '644',
        'needed_by': {
            f'svc_systemd:left4dead2-{server_name}.service',
        },
        'triggers': {
            f'svc_systemd:left4dead2-{server_name}.service:restart',
        },
    }

    svc_systemd[f'left4dead2-{server_name}.service'] = {
        'enabled': True,
        'running': True,
        'tags': {
            'left4dead2-servers',
        },
        'needs': {
            'svc_systemd:left4dead2-initialize.service',
            f'file:/usr/local/lib/systemd/system/left4dead2-{server_name}.service',
        },
    }
