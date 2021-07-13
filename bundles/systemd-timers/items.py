# svc_systemd['cron'] = {
#     'enabled': False,
# }

for name, config in node.metadata.get('systemd-timers').items():
    files[f'/etc/systemd/system/{name}.timer'] = {
        'content': repo.libs.systemd.generate_unitfile({
            'Unit':{
                'Description': f'{name} timer',
            },
            'Timer': {
                'OnCalendar': config['when'],
                'Persistent': config.get('persistent', False),
                'Unit': f'{name}.service',
            },
            'Install': {
                'WantedBy': 'multi-user.target',
            }
        }),
        'triggers': [
            'action:systemd-reload',
            f'svc_systemd:{name}:restart',
        ],
    }
    
    svc_systemd[f'{name}.timer'] = {}
