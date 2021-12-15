defaults = {
    'users': {
        'tasmota-charge': {
            'home': '/home/tasmota-charge',
        },
    },
    'systemd-timers': {
        'tasmota-charge': {
            'command': f'/usr/bin/sudo -u tasmota-charge /opt/tasmota-charge',
            'when': 'minutely',
        },
    },
}


@metadata_reactor.provides(
    'telegraf/config/inpus/exec',
)
def telegraf(metadata):
    return {
        'telegraf': {
            'config': {
                'inputs': {
                    'exec': {
                        repo.libs.hashable.hashable({
                            'commands': ["/usr/local/share/icinga/plugins/tasmota_charge"],
                            'name_override': "tasmota_charge",
                            'data_format': "influx",
                        }),
                    },
                },
            },
        },
    }
