{
    'in': {
        'stacked': True,
        'queries': {
            'in': {
                'filters': {
                    '_measurement': 'net',
                    '_field': [
                        'bytes_recv',
                    ],
                },
                'function': 'derivative',
            },
        },
        'unit': 'decbytes',
        'display_name': '__field.labels.interface'
    },
    'out': {
        'stacked': True,
        'queries': {
            'out': {
                'filters': {
                    '_measurement': 'net',
                    '_field': [
                        'bytes_sent',
                    ],
                },
                'function': 'derivative',
            },
        },
        'unit': 'decbytes',
        'display_name': '__field.labels.interface'
    },
}
