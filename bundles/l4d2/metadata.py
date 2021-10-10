defaults = {
    'steam': {
        'games': {
            'left4dead2': '222860',
        },
    },
    'left4dead2': {
        'serevrs': {},
    },
}


@metadata_reactor.provides(
    'systemd/units',
)
def steam(metadata):
    units = {}
    services = {}
    
    for name, config in metadata.get('left4dead2/servers').items():
        units[f'left4dead2-server-{name}.service'] = {
            'Unit': {
                'Description': 'steam: install and update games',
                'After': 'network.target',
                'Requires': 'steam-update.service',
            },
            'Service': {
                'User': 'steam',
                'Group': 'steam',
                'WorkingDirectory': '/opt/left4dead2',
                'ExecStart': f'/opt/left4dead2/srcds_run -port {config["port"]} -secure +exec /etc/left4dead2/{name}.cfg',
                'Restart': 'on-failure',
            },
            'Install': {
                'WantedBy': ['multi-user.target'],
            },
        }

    return {
        'systemd': {
            'units': units,
        },
    }
