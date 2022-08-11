{
    'cpu': {
        'queries': {
            'seome': {
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
        'display_name': '__field.labels.type',
        'unit': 'percent',
    },
    'memory': {
        'queries': {
            'some': {
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
            'full': {
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
        'display_name': '__field.labels.type',
        'unit': 'percent',
    },
    'io': {
        'queries': {
            'some': {
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
            'full': {
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
        },
        'display_name': '__field.labels.type',
        'unit': 'percent',
    },
}
