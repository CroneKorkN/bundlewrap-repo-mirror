defaults = {
    'apt': {
        'packages': {
            'lib32gcc-s1': {},
        },
    },
    'steam': {
        'games': {},
    }
}

@metadata_reactor.provides(
    'systemd/units',
)
def initial_unit(metadata):
    install_games = ' '.join(
        f'+force_install_dir /opt/{name} +app_update {id}'
            for name, id in metadata.get('steam/games').items()
    )
    
    return {
        'systemd': {
            'units': {
                'steam-update.service': {
                    'Unit': {
                        'Description': 'steam: install and update games',
                        'After': 'network.target',
                    },
                    'Service': {
                        'Type': 'oneshot',
                        'User': 'steam',
                        'Group': 'steam',
                        'WorkingDirectory': '/opt/steam',
                        'ExecStart': f'/opt/steam/steamcmd.sh +login anonymous {install_games} validate +quit',
                    },
                    'Install': {
                        'WantedBy': 'multi-user.target',
                    },
                },
            },
        },
    }
