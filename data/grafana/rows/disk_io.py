{
    'read': {
        'stacked': True,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'diskio',
                    '_field': [
                        'read_bytes',
                    ],
                },
                'function': 'derivative',
            },
        },
        'unit': 'decbytes',
        'display_name': '__field.labels.name',
        'tooltip': 'multi',
    },
    'write': {
        'stacked': True,
        'queries': {
            'load': {
                'filters': {
                    '_measurement': 'diskio',
                    '_field': [
                        'write_bytes',
                    ],
                },
                'function': 'derivative',
            },
        },
        'unit': 'decbytes',
        'display_name': '__field.labels.name',
        'tooltip': 'multi',
    },
}
