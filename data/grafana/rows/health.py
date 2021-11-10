{
    'temperature': {
        'stacked': False,
        'queries': {
            'cpu_temperature': {
                'filters': {
                    '_measurement': 'cpu_temperature',
                    '_field': [
                        'value',
                    ],
                },
                'function': 'mean',
            },
        },
        'unit': 'degrees',
    },
    'frequency': {
        'stacked': False,
        'queries': {
            'cpu_frequency': {
                'filters': {
                    '_measurement': 'cpu_frequency',
                    '_field': [
                        'current',
                    ],
                },
                'function': 'mean',
            },
        },
        'unit': 'MHz',
        'display_name': '__field.labels.cpu',
    },
}
