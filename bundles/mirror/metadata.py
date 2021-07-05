defaults = {
    'mirror': {},
}


@metadata_reactor.provides(
    'systemd-timers',
)
def timers(metadata):
    return {
        'systemd-timers': {
            f'mirror-{name}': {
                'command': f"/usr/bin/scp -r -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '{config['from']}' '{config['to']}'",
                'when': 'hourly',
            } for name, config in metadata.get('mirror').items()
        }
    }
