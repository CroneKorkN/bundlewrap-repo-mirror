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
                'exec': [{
                    'commands': [
                        f'sudo /usr/local/share/icinga/plugins/smartctl',
                    ],
                    'data_format': 'influx',
                    'interval': '60s',
                }],
            },
        },
    },
    'sudoers': {
        'telegraf': ['/usr/local/share/icinga/plugins/smartctl'],
    },
}
