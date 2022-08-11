{
    'avg10 some': {
        'queries': {
            'io': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'ressource': [
                        'io',
                    ],
                    'type': [
                        'some',
                    ],
                    '_field': [
                        'avg10',
                    ],
                },
            },
            'memory': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'ressource': [
                        'memory',
                    ],
                    'type': [
                        'some',
                    ],
                    '_field': [
                        'avg10',
                    ],
                },
            },
            'cpu': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'ressource': [
                        'cpu',
                    ],
                    'type': [
                        'some',
                    ],
                    '_field': [
                        'avg10',
                    ],
                },
            },
        },
        'display_name': '__field.labels.ressource',
        'unit': 'percent',
    },
    'avg10 full': {
        'queries': {
            'io': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'ressource': [
                        'io',
                    ],
                    'type': [
                        'full',
                    ],
                    '_field': [
                        'avg10',
                    ],
                },
            },
            'memory': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'ressource': [
                        'memory',
                    ],
                    'type': [
                        'full',
                    ],
                    '_field': [
                        'avg10',
                    ],
                },
            },
        },
        'display_name': '__field.labels.ressource',
        'unit': 'percent',
    },}
