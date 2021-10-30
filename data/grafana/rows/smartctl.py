{
    'temperature': {
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'smartctl',
                    '_field': [
                        'temperature',
                    ],
                },
                'function': 'mean',
            },
        },
        'display_name': '__field.labels.device',
        'min': 0,
        'unit': 'celsius',
    },
    'active': {
        'stacked': True,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'smartctl',
                    '_field': [
                        'active',
                    ],
                },
                'function': 'last',
                'boolean_to_int': True,
            },
        },
        'display_name': '__field.labels.device',
        'min': 0,
        'unit': 'active',
    },
}
