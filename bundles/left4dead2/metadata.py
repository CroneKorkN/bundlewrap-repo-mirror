from re import match


defaults = {
    'apt': {
        'packages': {
            'libc6_i386': {}, # installs libc6:i386
            'lib32z1': {},
            'unzip': {},
        },
    },
    'left4dead2': {},
    'nftables': {
        'input': {
            'udp dport { 27005, 27020 } accept',
        },
    },
    'systemd': {
        'units': {
            'left4dead2-initialize.service': {
                'Unit': {
                    'Description': 'initialize left4dead2',
                    'After': 'network-online.target',
                },
                'Service': {
                    'Type': 'oneshot',
                    'RemainAfterExit': 'yes',
                    'ExecStart': '/opt/l4d2/setup',
                    'StandardOutput': 'journal',
                    'StandardError': 'journal',
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

    for name, config in metadata.get('left4dead2').items():
        assert match(r'^[A-z0-9-_-]+$', name)
        assert config["overlay"] in {'pve', '100tick'}
        assert 27000 <= config["port"] <= 27100

        params = config.get("params", "")
        if config.get("tickrate"):
            params += f" -tickrate {config['tickrate']}"

        units[f'left4dead2-{name}.service'] = {
            'Unit': {
                'Description': f'left4dead2 server {name}',
                'After': {'left4dead2-initialize.service'},
                'Requires': {'left4dead2-initialize.service'},
            },
            'Service': {
                'Type': 'simple',
                'ExecStart': f'/opt/l4d2/start "{name}" "{config["overlay"]}" "{config["port"]}" "{params}"',
                'Restart': 'on-failure',
                'Nice': -10,
                'CPUWeight': 200,
                'IOSchedulingClass': 'best-effort',
                'IOSchedulingPriority': 0,
            },
            'Install': {
                'WantedBy': {'multi-user.target'},
            },
            'triggers': {
                f'svc_systemd:left4dead2-{name}.service:restart',
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
def nftables(metadata):
    ports = sorted(str(config["port"]) for config in metadata.get('left4dead2', {}).values())

    return {
        'nftables': {
            'input': {
                f'ip protocol {{ tcp, udp }} th dport {{ {", ".join(ports)} }} accept'
            },
        },
    }
