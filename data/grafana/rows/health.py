{
    'frequency': {
        'stacked': True,
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
        'legend': {
            'displayMode': 'hidden',
        },
        'tooltip': 'multi',
        'unit': 'MHz',
        'display_name': '__field.labels.cpu',
        'min': 0,
    },
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
        'legend': {
            'displayMode': 'hidden',
        },
        'tooltip': 'multi',
        'unit': 'degrees',
    },
    'sensors': {
        'stacked': False,
        'queries': {
            'sensors': {
                'filters': {
                    '_measurement': 'sensors',
                    '_field': [
                        'temp_input',
                    ],
                },
                'function': 'mean',
            },
        },
        'legend': {
            'displayMode': 'hidden',
        },
        'tooltip': 'multi',
        'unit': 'degrees',
        'display_name': '__field.labels.chip',
    },
}
