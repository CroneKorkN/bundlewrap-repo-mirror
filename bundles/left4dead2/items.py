assert node.has_bundle('steam') and node.has_bundle('steam-workshop-download')

directories = {
    '/opt/steam/left4dead2/left4dead2/ems/admin system': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '0755',
    },
    '/opt/steam/left4dead2/left4dead2/addons': {
        'owner': 'steam',
        'group': 'steam',
        'purge': True,
        'triggers': [
            *[f'svc_systemd:left4dead2-{name}.service:restart' for name in node.metadata.get('left4dead2/servers')],
        ],
    },
    '/opt/steam/left4dead2-servers': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '0755',
        'purge': True,
    },
    # Current zfs doesnt support zfs upperdir. The support was added in October 2022. Move upperdir - unused anyway -
    # to another dir. Also move workdir alongside it, as it has to be on same fs.
    '/opt/steam-zfs-overlay-workarounds': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '0755',
        'purge': True,
    },
}

files = {
    '/opt/steam/left4dead2/left4dead2/ems/admin system/admins.txt': {
        'owner': 'steam',
        'group': 'steam',
        'mode': '0755',
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

#
# SERVERS
#

for name, config in node.metadata.get('left4dead2/servers').items():

    #overlay
    directories[f'/opt/steam/left4dead2-servers/{name}'] = {
        'owner': 'steam',
        'group': 'steam',
    }
    directories[f'/opt/steam-zfs-overlay-workarounds/{name}/upper'] = {
        'owner': 'steam',
        'group': 'steam',
    }
    directories[f'/opt/steam-zfs-overlay-workarounds/{name}/workdir'] = {
        'owner': 'steam',
        'group': 'steam',
    }

    # conf
    files[f'/opt/steam/left4dead2-servers/{name}/left4dead2/cfg/server.cfg'] = {
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

    # addons
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
    for id in [
        *config.get('workshop', []),
        *node.metadata.get('left4dead2/workshop'),
    ]:
        files[f'/opt/steam/left4dead2-servers/{name}/left4dead2/addons/{id}.vpk'] = {
            'content_type': 'any',
            'owner': 'steam',
            'group': 'steam',
            'triggers': [
                f'svc_systemd:left4dead2-{name}.service:restart',
            ],
        }

    # service
    svc_systemd[f'left4dead2-{name}.service'] = {
        'needs': [
            f'file:/opt/steam/left4dead2-servers/{name}/left4dead2/cfg/server.cfg',
            f'file:/usr/local/lib/systemd/system/left4dead2-{name}.service',
        ],
    }
