directories = {
    '/etc/left4dead2': {
        'owner': 'steam',
        'purge': True,
    }
}

for name, config in node.metadata.get('left4dead2/servers').items():
    config.pop('port')
    config['sv_steamgroup'] = name
    config['hostname'] = name
    config['sv_steamgroup'] = ','.join(str(gid) for gid in  node.metadata.get('left4dead2/steamgroups'))

    files[f'/etc/left4dead2/{name}.cfg'] = {
        'content': '\n'.join(
            f'{key} "{value}"' for key, value in sorted(config.items())
        ) + '\n',
        'owner': 'steam',
        'triggers': [
            f'svc_systemd:left4dead2-server-{name}:restart',
        ],
    }
    svc_systemd[f'left4dead2-server-{name}'] = {
        'needs': [
            f'file:/etc/systemd/system/left4dead2-server-{name}.service',
        ],
    }

# TIDYUP

find_obsolete_units = (
    'find /etc/systemd/system -type f -name "left4dead2-server-*.service" ' +
    ' '.join(f"! -name '{service}.service'" for service in svc_systemd)
)
actions['remove_obsolete_left4dead2_units'] = {
    'command':  (
        f'for unitfile in $({find_obsolete_units}); '
        f'do '
            f'systemctl stop $(basename "$unitfile"); '
            f'systemctl disable $(basename "$unitfile"); '
            f'rm "$unitfile"; '
            f'systemctl daemon-reload; '
        f'done'
    ),
    'unless':    (
        find_obsolete_units + " | wc -l | grep -q '^0$'"
    ),
}
