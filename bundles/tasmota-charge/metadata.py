defaults = {
    'users': {
        'tasmota-charge': {
            'home': '/home/tasmota-charge',
        },
    },
    'systemd-timers': {
        'tasmota-charge': {
            'command': f'/opt/tasmota-charge',
            'when': 'minutely',
            'user': 'tasmota-charge',
        },
    },
}


@metadata_reactor.provides(
    'telegraf/config/inputs/exec',
)
def telegraf(metadata):
    return {
        'telegraf': {
            'config': {
                'inputs': {
                    'exec': {
                        repo.libs.hashable.hashable({
                            'commands': ["/usr/local/share/telegraf/tasmota_charge"],
                            'name_override': "tasmota_charge",
                            'data_format': "influx",
                        }),
                    },
                },
            },
        },
    }
