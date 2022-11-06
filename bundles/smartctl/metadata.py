h = repo.libs.hashable.hashable

defaults = {
    'apt': {
        'packages': {
            'smartmontools': {},
        },
    },
    'grafana_rows': {
        'smartctl',
    },
    'smartctl': {},
    'telegraf': {
        'config': {
            'inputs': {
                'exec': {
                    h({
                        'commands': [
                            f'sudo /usr/local/share/telegraf/smartctl_power_mode',
                        ],
                        'data_format': 'influx',
                        'interval': '20s',
                    }),
                    h({
                        'commands': [
                            f'sudo /usr/local/share/telegraf/smartctl_errors',
                        ],
                        'data_format': 'influx',
                        'interval': '6h',
                    })
                },
            },
        },
    },
    'sudoers': {
        'telegraf': {
            '/usr/local/share/telegraf/smartctl_power_mode',
            '/usr/local/share/telegraf/smartctl_errors',
        },
    },
}
