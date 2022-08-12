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
        'min': 0,
        'unit': 'bytes',
    },
    'hits': {
        'stacked': True,
        'queries': {
            'hits': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_demand_data_hits',
                        'arcstats_demand_metadata_hits',
                        'arcstats_prefetch_data_hits',
                        'arcstats_prefetch_metadata_hits',
                    ],
                },
                'function': 'derivative',
            },
        },
        'legend': {
            'displayMode': 'hidden',
        },
        'tooltip': 'multi',
    },
    'misses': {
        'stacked': True,
        'queries': {
            'misses': {
                'filters': {
                    '_measurement': 'zfs',
                    '_field': [
                        'arcstats_demand_data_misses',
                        'arcstats_demand_metadata_misses',
                        'arcstats_prefetch_data_misses',
                        'arcstats_prefetch_metadata_misses',
                    ],
                },
                'function': 'derivative',
            },
        },
        'legend': {
            'displayMode': 'hidden',
        },
        'tooltip': 'multi',
    },
    'l2': {
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
        'unit': 'Bps',
    },
}
