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
        'display_name': '__field.labels.name'
    },
}
