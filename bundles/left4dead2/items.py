assert node.has_bundle('steam') and node.has_bundle('steam-workshop-download')

directories = {
    '/opt/steam/left4dead2/left4dead2/ems/admin system': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '0744',
    },
    '/opt/steam/left4dead2/left4dead2/cfg/server': {
        'owner': 'steam',
        'group': 'steam',
        'purge': True,
    },
    '/opt/steam/left4dead2/left4dead2/addons': {
        'owner': 'steam',
        'group': 'steam',
        'purge': True,
        'triggers': [
            *[f'svc_systemd:left4dead2-{name}.service:restart' for name in node.metadata.get('left4dead2/servers')],
        ],
    },
    # Current zfs doesnt support zfs upperdir. The support was added in October 2022. Move upperdir - unused anyway -
    # to another dir. Also move workdir alongside it, as it has to be on same fs.
    '/opt/steam-zfs-overlay-workarounds': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '0744',
    },
}

files = {
    '/opt/steam/left4dead2/left4dead2/ems/admin system/admins.txt': {
        'owner': 'steam',
        'content': '\n'.join(sorted(node.metadata.get('left4dead2/admins'))),
    },
    '/opt/steam/left4dead2/left4dead2/addons/readme.txt': {
        'content_type': 'any',
        'owner': 'steam',
        'group': 'steam',
    }
}

for id in node.metadata.get('left4dead2/workshop'):
    files[f'/opt/steam/left4dead2/left4dead2/addons/{id}.vpk'] = {
        'content_type': 'any',
        'owner': 'steam',
        'group': 'steam',
        'triggers': [
            *[f'svc_systemd:left4dead2-{name}.service:restart' for name in node.metadata.get('left4dead2/servers')],
        ],
    }

# /opt/steam/steam/.steam/sdk32/steamclient.so: cannot open shared object file: No such file or directory
symlinks = {
    '/opt/steam/steam/.steam/sdk32': {
        'target': '/opt/steam/steam/linux32',
        'owner': 'steam',
        'group': 'steam',
    }
}

for name, config in node.metadata.get('left4dead2/servers').items():
    directories[f'/opt/steam/left4dead2-servers/{name}'] = {}
    directories[f'/opt/steam-zfs-overlay-workarounds/{name}/upper'] = {}
    directories[f'/opt/steam-zfs-overlay-workarounds/{name}/workdir'] = {}

    files[f'/opt/steam/left4dead2/left4dead2/cfg/server/{name}.cfg'] = {
        'content_type': 'mako',
        'source': 'server.cfg',
        'context': {
            'name': name,
            'steamgroups': node.metadata.get('left4dead2/steamgroups'),
            'rcon_password': config['rcon_password'],
        },
        'owner': 'steam',
        'group': 'steam',
        'triggers': [
            f'svc_systemd:left4dead2-{name}.service:restart',
        ],
    }
    svc_systemd[f'left4dead2-{name}.service'] = {
        'needs': [
            f'file:/opt/steam/left4dead2/left4dead2/cfg/server/{name}.cfg',
            f'file:/usr/local/lib/systemd/system/left4dead2-{name}.service',
        ],
    }
    directories[f'/opt/steam/left4dead2-servers/{name}/left4dead2/addons'] = {
        'owner': 'steam',
        'group': 'steam',
        'purge': True,
        'triggers': [
            f'svc_systemd:left4dead2-{name}.service:restart',
        ],
    }
    files[f'/opt/steam/left4dead2-servers/{name}/left4dead2/addons/readme.txt'] = {
        'content_type': 'any',
        'owner': 'steam',
        'group': 'steam',
    }
    for id in node.metadata.get('left4dead2/workshop'):
        files[f'/opt/steam/left4dead2-servers/{name}/left4dead2/addons/{id}.vpk'] = {
            'content_type': 'any',
            'owner': 'steam',
            'group': 'steam',
            'triggers': [
                f'svc_systemd:left4dead2-{name}.service:restart',
            ],
        }

