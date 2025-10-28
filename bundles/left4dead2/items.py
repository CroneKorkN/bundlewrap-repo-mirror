files = {
    '/opt/l4d2/setup': {
        'mode': '755',
        'triggers': {
            'svc_systemd:left4dead2-initialize.service:restart',
        },
    },
    '/opt/l4d2/start': {
        'mode': '755',
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

for server_name in node.metadata.get('left4dead2').keys():
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
