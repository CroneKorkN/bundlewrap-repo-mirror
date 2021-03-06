{
    'usage': {
        'stacked': False,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'cpu',
                    'cpu': 'cpu-total',
                    '_field': [
                        'usage_guest',
                        'usage_guest_nice',
                        'usage_iowait',
                        'usage_irq',
                        'usage_nice',
                        'usage_softirq',
                        'usage_steal',
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
