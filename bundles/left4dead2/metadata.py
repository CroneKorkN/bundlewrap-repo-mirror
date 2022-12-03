assert node.has_bundle('steam')

from shlex import quote

defaults = {
    'steam': {
        'games': {
            'left4dead2': 222860,
        },
    },
    'left4dead2': {
        'servers': {},
        'admins': set(),
        'workshop': set(),
    },
}


@metadata_reactor.provides(
    'left4dead2/servers',
)
def rconn_password(metadata):
    # only works from localhost!
    return {
        'left4dead2': {
            'servers': {
                server: {
                    'rcon_password': repo.vault.password_for(f'{node.name} left4dead2 {server} rcon', length=24),
                }
                    for server in metadata.get('left4dead2/servers')
            },
        },
    }


@metadata_reactor.provides(
    'steam-workshop-download',
)
def workshop_download(metadata):
    if metadata.get('left4dead2/workshop'):
        return {
            'steam-workshop-download': {
                'left4dead2-global': {
                    'ids': metadata.get('left4dead2/workshop'),
                    'path': '/opt/steam/left4dead2/left4dead2/addons',
                    'user': 'steam',
                    'requires': {
                        'steam-update.service',
                    },
                    'required_by': {
                        f'left4dead2-{name}.service'
                            for name in metadata.get('left4dead2/servers')
                    },
                },
            },
        }
    else:
        return {}


@metadata_reactor.provides(
    'steam-workshop-download',
    'systemd/units',
)
def server_units(metadata):
    units = {}
    workshop = {}

    for name, config in metadata.get('left4dead2/servers').items():
        # mount overlay
        mountpoint = f'/opt/steam/left4dead2-servers/{name}'
        mount_unit_name = mountpoint[1:].replace('-', '\\x2d').replace('/', '-') + '.mount'
        units[mount_unit_name] = {
            'Unit': {
                'Description': f"Mount left4dead2 server {name} overlay",
                'Conflicts': {'umount.target'},
                'Before': {'umount.target'},
            },
            'Mount': {
                'What': 'overlay',
                'Where': mountpoint,
                'Type': 'overlay',
                'Options': ','.join([
                    'auto',
                    'lowerdir=/opt/steam/left4dead2',
                    f'upperdir=/opt/steam-zfs-overlay-workarounds/{name}/upper',
                    f'workdir=/opt/steam-zfs-overlay-workarounds/{name}/workdir',
                ]),
            },
            'Install': {
                'RequiredBy': {
                    f'left4dead2-{name}.service',
                },
            },
        }

        # individual workshop
        if 'workshop' in config:
            workshop[f'left4dead2-{name}'] = {
                'ids': config['workshop'],
                'path': f'/opt/steam/left4dead2-servers/{name}/left4dead2/addons',
                'user': 'steam',
                'requires': {
                    mount_unit_name,
                },
                'required_by': {
                    f'left4dead2-{name}.service',
                },
            }

        # left4dead2 server unit
        units[f'left4dead2-{name}.service'] = {
            'Unit': {
                'Description': f'left4dead2 server {name}',
                'After': {'steam-update.service'},
                'Requires': {'steam-update.service'},
            },
            'Service': {
                'User': 'steam',
                'Group': 'steam',
                'WorkingDirectory': f'/opt/steam/left4dead2-servers/{name}',
                'ExecStart': f'/opt/steam/left4dead2-servers/{name}/srcds_run -port {config["port"]} +exec server.cfg',
                'Restart': 'on-failure',
            },
            'Install': {
                'WantedBy': {'multi-user.target'},
            },
        }

    return {
        'steam-workshop-download': workshop,
        'systemd': {
            'units': units,
        },
    }


@metadata_reactor.provides(
    'nftables/input',
)
def firewall(metadata):
    ports = set(str(server['port']) for server in metadata.get('left4dead2/servers').values())

    return {
        'nftables': {
            'input': {
                f"tcp dport {{ {', '.join(sorted(ports))} }} accept",
                f"udp dport {{ {', '.join(sorted(ports))} }} accept",
            },
        },
    }
