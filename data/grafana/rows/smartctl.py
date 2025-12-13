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
        'display_name': '${__field.labels.device}',
        'min': 0,
        'unit': 'celsius',
        'tooltip': 'multi',
    },
    'power_level': {
        'stacked': True,
        'queries': {
            'power_level': {
                'filters': {
                    '_measurement': 'smartctl',
                    '_field': [
                        'power_level',
                    ],
                },
                'function': 'last',
            },
        },
        'display_name': '${__field.labels.device}',
        'min': 0,
        'tooltip': 'multi',
    },
    'errors': {
        'stacked': True,
        'queries': {
            'power_level': {
                'filters': {
                    '_measurement': 'smart_errors',
                },
            },
        },
        'display_name': '${__field.labels.device} ${__field.name}',
        'min': 0,
        'tooltip': 'multi',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
