from re import match
from os import path, listdir


defaults = {
    'apt': {
        'packages': {
            'libc6_i386': {}, # installs libc6:i386
            'lib32z1': {},
            'unzip': {},
            'p7zip-full': {}, # l4d2center_maps_sync.sh
        },
    },
    'left4dead2': {
        'overlays': set(listdir(path.join(repo.path, 'bundles/left4dead2/files/scripts/overlays'))),
        'servers': {
            # 'port': 27017,
            # 'overlays': ['competitive_rework'],
            # 'arguments': ['-tickrate 60'],
            # 'config': [
            #     'exec server_original.cfg',
            #     'sm_forcematch zonemod',
            # ],
        },
    },
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

    for name, config in metadata.get('left4dead2/servers').items():
        assert match(r'^[A-z0-9-_-]+$', name)
        assert 27000 <= config["port"] <= 27100
        for overlay in config.get('overlays', []):
            assert overlay in metadata.get('left4dead2/overlays'), f"unknown overlay {overlay}, known: {metadata.get('left4dead2/overlays')}"

        cmd = f'/opt/l4d2/start -n {name} -p {config["port"]}'

        if 'config' in config:
            cmd += f' -c /opt/l4d2/configs/{name}.cfg'

        for overlay in config.get('overlays', []):
            cmd += f' -o {overlay}'

        if 'arguments' in config:
            cmd += ' -- ' + ' '.join(config['arguments'])

        units[f'left4dead2-{name}.service'] = {
            'Unit': {
                'Description': f'left4dead2 server {name}',
                'After': {'left4dead2-initialize.service'},
                'Requires': {'left4dead2-initialize.service'},
            },
            'Service': {
                'Type': 'simple',
                'ExecStart': cmd,
                'ExecStop': f'/opt/l4d2/stop -n {name}',
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
    ports = sorted(str(config["port"]) for config in metadata.get('left4dead2/servers').values())

    return {
        'nftables': {
            'input': {
                f'ip protocol {{ tcp, udp }} th dport {{ {", ".join(ports)} }} accept'
            },
        },
    }
