defaults = {
    'apt': {
        'packages': {
            'apcupsd': {},
        },
    },
    'grafana_rows': {
        'ups',
    },
    'sudoers': {
        'telegraf': ['/usr/local/share/telegraf/apcupsd'],
    },
    'telegraf': {
        'config': {
            'inputs': {
                'exec': {
                    repo.libs.hashable.hashable({
                        'commands': ["sudo /usr/local/share/telegraf/apcupsd"],
                        'name_override': "apcupsd",
                        'data_format': "influx",
                    }),
                },
            },
        },
    },
}
