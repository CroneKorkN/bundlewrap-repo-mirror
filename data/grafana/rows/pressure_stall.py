{
    'cpu': {
        'queries': {
            'seome': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'resource': [
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
                    'resource': [
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
                    'resource': [
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
                    'resource': [
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
                    'resource': [
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
