directories = {}

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
    directories[f'/opt/l4d2/servers/{server_name}'] = {
        'owner': 'steam',
        'mode': '755',
        'needed_by': {
            f'svc_systemd:left4dead2-{server_name}.service',
        },
    }

    files[f'/opt/l4d2/servers/{server_name}/server.cfg'] = {#
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
