{
    'root_usage': {
        'stacked': True,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'disk',
                    'path': '/',
                    '_field': [
                        'used',
                        'free',
                    ],
                },
                'function': 'mean',
            },
        },
        'min': 0,
        'unit': 'bytes',
    },
    'root_inodes': {
        'stacked': True,
        'queries': {
            'inodes': {
                'filters': {
                    '_measurement': 'disk',
                    'path': '/',
                    '_field': [
                        'inodes_used',
                        'inodes_free',
                    ],
                },
                'function': 'mean',
            },
        },
        'min': 0,
    },
}
