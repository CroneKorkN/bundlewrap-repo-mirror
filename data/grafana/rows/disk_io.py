{
    'read': {
        'stacked': True,
        'queries': {
            'usage': {
                'filters': {
                    '_measurement': 'diskio',
                    '_field': [
                        'read_bytes',
                    ],
                },
                'exists': [
                    'ID_PART_ENTRY_NUMBER',
                ],
                'function': 'derivative',
            },
        },
        'unit': 'Bps',
        'display_name': '__field.labels.name',
        'tooltip': 'multi',
    },
    'write': {
        'stacked': True,
        'queries': {
            'load': {
                'filters': {
                    '_measurement': 'diskio',
                    '_field': [
                        'write_bytes',
                    ],
                },
                'exists': [
                    'ID_PART_ENTRY_NUMBER',
                ],
                'function': 'derivative',
            },
        },
        'unit': 'Bps',
        'display_name': '__field.labels.name',
        'tooltip': 'multi',
    },
}
