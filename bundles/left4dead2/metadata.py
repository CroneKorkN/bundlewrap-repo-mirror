assert node.has_bundle('steam')

from shlex import quote

defaults = {
    'steam': {
        'games': {
            'left4dead2': '222860',
        },
    },
    'left4dead2': {
        'servers': {},
        'admins': set(),
        'workshop': set(),
    },
}


@metadata_reactor.provides(
    'systemd/units',
)
def workshop(metadata):
    command = (
        'set -x; '
        'for ID in ' + ' '.join(metadata.get('left4dead2/workshop')) + '; '
        'do '
            'if ! ls /opt/left4dead2/left4dead2/addons/$ID/*.vpk; '
            'then '
                'cd /opt/left4dead2/left4dead2/addons/$ID; '
                '/opt/steam-workshop-downloader https://steamcommunity.com/sharedfiles/filedetails\?id\=$ID; '
                'unzip $ID.zip; '
            'fi; '
        'done'
    )
    
    return {
        'systemd': {
            'units': {
                'left4dead2-workshop.service': {
                    'Unit': {
                        'Description': 'install workshop items',
                        'After': 'network.target',
                        'Requires': 'steam-update.service',
                        'PartOf': 'steam-update.service'
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'User': 'steam',
                        'ExecStart': f'/bin/bash -c {quote(command)}',
                    },
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    },
                }
            }
        }
    }


@metadata_reactor.provides(
    'systemd/units',
)
def server_units(metadata):
    units = {}
    
    for name, config in metadata.get('left4dead2/servers').items():
        units[f'left4dead2-server-{name}.service'] = {
            'Unit': {
                'Description': f'left4dead2 server {name}',
                'After': 'network.target',
                'Requires': 'steam-update.service',
            },
            'Service': {
                'User': 'steam',
                'Group': 'steam',
                'WorkingDirectory': '/opt/left4dead2',
                'ExecStart': f'/opt/left4dead2/srcds_run -port {config["port"]} -insecure +map {config["map"]} +exec server-{name}.cfg',
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
