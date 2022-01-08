defaults = {
    'apt': {
        'packages': {
            'lm-sensors': {},
        },
    },
    'grafana_rows': {
        'health',
    },
    'sudoers': {
        'telegraf': {
            '/usr/local/share/telegraf/cpu_frequency',
        },
    },
    'telegraf': {
        'config': {
            'inputs': {
                'sensors': {repo.libs.hashable.hashable({
                    'timeout': '2s',
                })},
                'exec': {
                    repo.libs.hashable.hashable({
                        'commands': ["sudo /usr/local/share/telegraf/cpu_frequency"],
                        'name_override': "cpu_frequency",
                        'data_format': "influx",
                    }),
                    # repo.libs.hashable.hashable({
                    #     'commands': ["/bin/bash -c 'expr $(cat /sys/class/thermal/thermal_zone0/temp) / 1000'"],
                    #     'name_override': "cpu_temperature",
                    #     'data_format': "value",
                    #     'data_type': "integer",
                    # }),
                },
            },
        },
    },
}
