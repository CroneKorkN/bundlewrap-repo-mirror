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
    },
}
