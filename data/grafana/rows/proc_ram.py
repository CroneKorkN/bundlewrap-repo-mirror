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
                'resolution': 6,
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
