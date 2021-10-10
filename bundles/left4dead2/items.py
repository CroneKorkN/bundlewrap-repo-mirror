directories = {
    '/opt/left4dead2': {
        'owner': 'steam',
    },
    '/opt/left4dead2/ems/admin system': {
        'owner': 'steam',
    },
    '/opt/left4dead2/addons': {
        'owner': 'steam',
        'purge': True,
    },
    '/etc/left4dead2': {
        'owner': 'steam',
        'purge': True,
    },
}

files = {
    '/opt/left4dead2/ems/admin system/admins.txt': {
        'owner': 'steam',
        'content': '\n'.join(node.metadata.get('left4dead2/admins')),
    }
}

svc_systemd = {
    'left4dead2-workshop': {
        'running': False,
        'needs': [
            'svc_systemd:steam-update',
        ],
    },
}

for id in node.metadata.get('left4dead2/workshop'):
    directories[f'/opt/left4dead2/addons/{id}'] = {
        'owner': 'steam',
        'triggers': [
            'svc_systemd:left4dead2-workshop:restart',
        ],
    }

server_units = set()
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
    server_units.add(f'left4dead2-server-{name}')
    

for id in node.metadata.get('left4dead2/workshop'):
    directories[f'/opt/left4dead2/addons/{id}'] = {
        'owner': 'steam',
        'triggers': [
            'svc_systemd:left4dead2-workshop:restart',
        ],
    }

# TIDYUP

find_obsolete_units = (
    'find /etc/systemd/system -type f -name "left4dead2-server-*.service" ' +
    ' '.join(f"! -name '{name}.service'" for name in server_units)
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
