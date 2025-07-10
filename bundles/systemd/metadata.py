defaults = {
    'systemd': {
        'units': {},
        'services': {},
        'logind': {},
    },
    'monitoring': {
        'services': {
            'systemd': {
                'vars.command': "systemctl --failed --no-legend | wc -l | grep -q '^0$' && exit 0 || systemctl --failed && exit 2",
            },
        },
    },
}

@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    units = {}

    for name, config in metadata.get('systemd/units').items():
        if '/' in name:
            continue

        type = name.split('.')[-1]

        if type == 'service':
            if not config.get('Install', {}).get('WantedBy', set()):
                units.setdefault(name, {}).setdefault('Install', {}).setdefault('WantedBy', {'multi-user.target'})
        elif type == 'timer':
            units.setdefault(name, {}).setdefault('Install', {}).setdefault('WantedBy', {'timers.target'})
        elif type == 'mount':
            units.setdefault(name, {}).setdefault('Install', {}).setdefault('WantedBy', {'local-fs.target'})
            units.setdefault(name, {}).setdefault('Unit', {}).setdefault('Conflicts', {'umount.target'})
            units.setdefault(name, {}).setdefault('Unit', {}).setdefault('Before', {'umount.target'})

    return {
        'systemd': {
            'units': units,
        }
    }


@metadata_reactor.provides(
    'systemd/services',
)
def services(metadata):
    services = {}

    for name, config in metadata.get('systemd/services').items():
        extension = name.split('.')[-1]

        if extension not in ['timer', 'service', 'mount', 'swap']:
            raise Exception(f'unknown extension: {extension}')

    return {
        'systemd': {
            'services': services,
        }
    }


@metadata_reactor.provides(
    'monitoring/services',
)
def monitoring(metadata):
    return {
        'monitoring': {
            'services': {
                name: {
                    'vars.command': f"/bin/sh -c '/usr/bin/systemctl is-failed {name} && /usr/bin/systemctl status {name} && exit 2 || exit 0'"
                }
                    for name in metadata.get('systemd/units')
                    if name.endswith('.service')
            },
        },
    }
