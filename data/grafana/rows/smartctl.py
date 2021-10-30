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
        'min': 0,
        'unit': 'degrees',
    },
}
