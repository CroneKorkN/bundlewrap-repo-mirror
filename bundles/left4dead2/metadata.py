from re import match

defaults = {
    'apt': {
        'packages': {
            'libc6_i386': {}, # installs libc6:i386
            'lib32z1': {},
            'unzip': {},
        },
    },
    'left4dead2': {
        'servers': {},
    },
    'nftables': {
        'input': {
            'udp dport { 27005, 27020 } accept',
        },
    },
}


@metadata_reactor.provides(
    'nftables/input',
)
def nftables(metadata):
    ports = sorted(str(config["port"]) for config in metadata.get('left4dead2/servers', {}).values())

    return {
        'nftables': {
            'input': {
                f'ip protocol {{ tcp, udp }} th dport {{ {", ".join(ports)} }} accept'
            },
        },
    }


@metadata_reactor.provides(
    'systemd/units',
)
def initial_unit(metadata):
    install_command = (
        '/opt/steam/steamcmd.sh '
        '+force_install_dir /opt/left4dead2 '
        '+login anonymous '
        '+@sSteamCmdForcePlatformType {platform} '
        '+app_update 222860 validate '
        '+quit '
    )

    return {
        'systemd': {
            'units': {
                'left4dead2-install.service': {
                    'Unit': {
                        'Description': 'install or update left4dead2',
                        'After': 'network-online.target',
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'RemainAfterExit': 'yes',
                        'User': 'steam',
                        'Group': 'steam',
                        'WorkingDirectory': '/opt/steam',
                        'ExecStartPre': install_command.format(platform='windows'),
                        'ExecStart': install_command.format(platform='linux'),
                    },
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'systemd/units',
)
def server_units(metadata):
    units = {}

    for name, config in metadata.get('left4dead2/servers').items():
        assert match(r'^[A-z0-9-_-]+$', name)

        units[f'left4dead2-{name}.service'] = {
            'Unit': {
                'Description': f'left4dead2 server {name}',
                'After': {'left4dead2-install.service'},
                'Requires': {'left4dead2-install.service'},
            },
            'Service': {
                'User': 'steam',
                'Group': 'steam',
                'WorkingDirectory': '/opt/left4dead2',
                'ExecStart': f'/opt/left4dead2/srcds_run -port {config["port"]} +exec server_{name}.cfg',
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
