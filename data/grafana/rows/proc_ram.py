{
    'process_ram': {
        'stacked': True,
        'queries': {
            'ram': {
                'filters': {
                    '_measurement': 'procstat',
                    '_field': [
                        'memory_rss',
                    ],
                },
                'minimum': 10*(10**6),
            },
        },
        'unit': 'bytes',
        'display_name': '__field.labels.process_name',
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
