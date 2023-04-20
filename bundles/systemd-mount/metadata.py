defaults = {
    'apt': {
        'packages': {
            'bindfs': {},
        },
    },
    'systemd-mount': {},
}


@metadata_reactor.provides(
    'systemd/units',
    'systemd/services',
)
def units(metadata):
    units = {}
    services = {}

    for mountpoint, conf in metadata.get('systemd-mount').items():
        formatted_name = mountpoint[1:].replace('-', '\\x2d').replace('/', '-') + '.mount'

        units[formatted_name] = {
            'Unit': {
                'Description': f"Mount {conf['source']} -> {mountpoint}",
                'DefaultDependencies': 'no',
            },
            'Mount': {
                'What': conf['source'],
                'Where': mountpoint,
                'Type': 'fuse.bindfs',
                'Options': f"nonempty",
            },
        }

        if conf.get('user'):
            units[formatted_name]['Mount']['Options'] += f",force-user={conf.get('user')}"

        services[formatted_name] = {}

    return {
        'systemd': {
            'units': units,
            'services': services,
        }
    }


@metadata_reactor.provides(
    'systemd/units',
)
def zfs(metadata):
    return {
        'systemd': {
            'units': {
                name: {
                    'Unit': {
                        'After': 'zfs-mount.service',
                        'Requires': 'zfs-mount.service',
                    },
                }
                    for name in metadata.get('systemd/units')
                    if name.endswith('.mount')
            },
        }
    }
