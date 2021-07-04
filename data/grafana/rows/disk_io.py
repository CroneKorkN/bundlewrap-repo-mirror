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
        'display_name': '__field.labels.name'
    },
    'write': {
        'stacked': False,
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
        'display_name': '__field.labels.name'
    },
}
