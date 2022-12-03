from shlex import quote


defaults = {
    'steam-workshop-download': {},
}


@metadata_reactor.provides(
    'systemd/units',
)
def workshop(metadata):
    units = {}

    for name, conf in metadata.get('steam-workshop-download').items():
        units[f'steam-workshop-download-{name}.service'] = {
            'Unit': {
                'Description': 'install workshop items',
                'After': {
                    'network-online.target',
                    'steam-update.target',
                },
                'Before': 'steam-update.service',
                'Requires': conf['requires'],
            },
            'Service': {
                'Type': 'oneshot',
                'User': conf['user'],
                'ExecStart': f"/opt/steam-workshop-download {' '.join(quote(str(id)) for id in conf['ids'])} --out {quote(conf['path'])}",
            },
            'Install': {
                'RequiredBy': conf['required_by'],
            },
        }

    return {
        'systemd': {
            'units': units,
        },
    }
