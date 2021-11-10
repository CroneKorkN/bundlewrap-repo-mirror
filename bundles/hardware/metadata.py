defaults = {
    'sudoers': {
        'telegraf': {
            '/usr/local/share/icinga/plugins/cpu_frequency',
        },
    },
    'telegraf': {
        'config': {
            'inputs': {
                'exec': {
                    repo.libs.hashable.hashable({
                        'commands': ["sudo /usr/local/share/icinga/plugins/cpu_frequency"],
                        'name_override': "cpu_frequency",
                        'data_format': "influx",
                    }),
                },
            },
        },
    },
}
