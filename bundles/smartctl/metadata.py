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
                'exec': {h({
                    'commands': [
                        f'sudo /usr/local/share/icinga/plugins/smartctl',
                    ],
                    'data_format': 'influx',
                    'interval': '20s',
                })},
            },
        },
    },
    'sudoers': {
        'telegraf': ['/usr/local/share/icinga/plugins/smartctl'],
    },
}
