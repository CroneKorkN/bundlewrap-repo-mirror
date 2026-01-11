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
        'inputs': {
            'exec': {
                'smartctl_power_mode': {
                    'commands': [
                        f'sudo /usr/local/share/telegraf/smartctl_power_mode',
                    ],
                    'data_format': 'influx',
                    'interval': '20s',
                },
                'smartctl_errors': {
                    'commands': [
                        f'sudo /usr/local/share/telegraf/smartctl_errors',
                    ],
                    'data_format': 'influx',
                    'interval': '6h',
                }
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
