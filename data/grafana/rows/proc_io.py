{
    'io_read': {
        'stacked': True,
        'queries': {
            'io_read': {
                'filters': {
                    '_measurement': 'procio',
                    '_field': [
                        'read_bytes',
                    ],
                },
                'function': 'derivative',
                'minimum': 1,
            },
        },
        'unit': 'bytes',
        'display_name': '__field.labels.comm',
        'legend': {
            'displayMode': 'table',
            'placement': 'right',
            'calcs': [
                'mean',
                'max',
            ],
        },
    },
    'io_write': {
        'stacked': True,
        'queries': {
            'io_write': {
                'filters': {
                    '_measurement': 'procio',
                    '_field': [
                        'write_bytes',
                    ],
                },
                'function': 'derivative',
                'minimum': 1,
            },
        },
        'unit': 'bytes',
        'display_name': '__field.labels.comm',
        'legend': {
            'displayMode': 'table',
            'placement': 'right',
            'calcs': [
                'mean',
                'max',
            ],
        },
    },
}
