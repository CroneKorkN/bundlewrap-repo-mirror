{
    'usage': {
        'stacked': False,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'cpu',
                    'cpu': 'cpu-total',
                    '_field': [
                        'usage_iowait',
                        'usage_system',
                        'usage_user',
                    ],
                },
                'function': 'mean',
            },
        },
        'min': 0,
        'max': 100,
    },
    'load': {
        'stacked': False,
        'queries': {
            'load': {
                'filters': {
                    '_measurement': 'system',
                    '_field': [
                        'load1',
                        'load5',
                        'load15',
                    ],
                },
                'function': 'mean',
            },
        },
    },
}
