defaults = {
    'apt': {
        'packages': {
            'lib32gcc-s1': {},
            'unzip': {},
        },
    },
    'steam': {
        'games': {
            'left4dead2': 222860,
        },
    },
    'zfs': {
        'datasets': {
            'tank/steam': {
                'mountpoint': '/opt/steam',
                'backup': False,
            },
        },
    },
}


@metadata_reactor.provides(
    'systemd/units',
)
def initial_unit(metadata):
    return {
        'systemd': {
            'units': {
                'steam-update.service': {
                    'Unit': {
                        'Description': 'steam: install and update games',
                        'After': 'network-online.target',
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'User': 'steam',
                        'Group': 'steam',
                        'WorkingDirectory': '/opt/steam',
                        'ExecStart': {
                            f'/opt/steam/steam/steamcmd.sh +force_install_dir /opt/steam/{game} +login anonymous +app_update {id} validate +quit'
                                for game, id in metadata.get('steam/games').items()
                        }
                    },
                    'Install': {
                        'WantedBy': {'multi-user.target'},
                    },
                },
            },
        },
    }
