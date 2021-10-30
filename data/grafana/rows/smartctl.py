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
        'unit': 'degrees',
    },
}
