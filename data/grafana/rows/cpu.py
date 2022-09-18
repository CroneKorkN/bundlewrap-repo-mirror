{
    'usage': {
        'stacked': True,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'cpu',
                    'cpu': 'cpu-total',
                    '_field': [
                        'usage_guest',
                        'usage_guest_nice',
                        'usage_iowait',
                        'usage_irq',
                        'usage_nice',
                        'usage_softirq',
                        'usage_steal',
                        'usage_system',
                        'usage_user',
                    ],
                },
                'function': 'mean',
            },
        },
        'min': 0,
        'soft_max': 3,
        'unit': 'percent',
        'tooltip': 'multi',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'pressure_stall': {
        'stacked': True,
        'queries': {
            'pressure_stall': {
                'filters': {
                    '_measurement': 'pressure_stall',
                    'resource': [
                        'cpu',
                        'io',
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
        },
        'min': 0,
        'soft_max': 3,
        'display_name': '__field.labels.resource',
        'unit': 'percent',
        'tooltip': 'multi',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
