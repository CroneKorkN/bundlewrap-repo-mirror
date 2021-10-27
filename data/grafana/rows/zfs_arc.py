{
    'size': {
        'queries': {
            'size': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_metadata_size',
                        'arcstats_data_size',
                        'arcstats_l2_size',
                    ],
                },
                'function': 'mean',
            },
        },
        'unit': 'bytes',
    },
    'hits': {
        'queries': {
            'hits': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_hits',
                    ],
                },
                'function': 'derivative',
            },
            'misses': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_misses',
                    ],
                },
                'function': 'derivative',
                'negative': True,
            },
        },
    },
    'l2_hits': {
        'queries': {
            'hits': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_l2_hits',
                    ],
                },
                'function': 'derivative',
            },
            'misses': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_l2_misses',
                    ],
                },
                'function': 'derivative',
                'negative': True,
            },
        },
    },
    'l2_io': {
        'queries': {
            'read': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_l2_read_bytes',
                    ],
                },
                'function': 'derivative',
            },
            'write': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_l2_write_bytes',
                    ],
                },
                'function': 'derivative',
                'negative': True,
            },
        },
        'unit': 'bytes',
    },
}
