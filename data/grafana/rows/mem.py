{
    'memory': {
        'stacked': True,
        'queries': {
            'memory': {
                'filters': {
                    '_measurement': 'mem',
                    '_field': [
                        'used',
                        'cached',
                        'buffered',
                        'free',
                    ],
                },
                'function': 'mean',
            },
        },
        'unit': 'decbytes',
        'tooltip': 'multi',
    },
    'swp': {
        'stacked': True,
        'queries': {
            'memory': {
                'filters': {
                    '_measurement': 'mem',
                    '_field': [
                        'swap_cached',
                        'swap_free',
                    ],
                },
                'function': 'mean',
            },
        },
        'unit': 'decbytes',
        'tooltip': 'multi',
    },
}
