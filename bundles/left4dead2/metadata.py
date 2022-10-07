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
    'steam-workshop-download/left4dead',
)
def workshop_download(metadata):
    if not metadata.get('left4dead2/workshop'):
        return {}

    return {
        'steam-workshop-download': {
            'left4dead': {
                'ids': metadata.get('left4dead2/workshop'),
                'path': '/opt/steam/left4dead2/left4dead2/addons',
                'user': 'steam',
            },
        },
    }


@metadata_reactor.provides(
    'systemd/units',
)
def server_units(metadata):
    units = {}

    for name, config in metadata.get('left4dead2/servers').items():
        units[f'left4dead2-{name}.service'] = {
            'Unit': {
                'Description': f'left4dead2 server {name}',
                'After': {'steam.target'},
            },
            'Service': {
                'User': 'steam',
                'Group': 'steam',
                'WorkingDirectory': '/opt/steam/left4dead2',
                'ExecStart': f'/opt/steam/left4dead2/srcds_run -port {config["port"]} +exec server/{name}.cfg',
                'Restart': 'on-failure',
            },
            'Install': {
                'WantedBy': {'multi-user.target'},
            },
        }

    return {
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
                f"tcp dport {{ {', '.join(ports)} }} accept",
                f"udp dport {{ {', '.join(ports)} }} accept",
            },
        },
    }
