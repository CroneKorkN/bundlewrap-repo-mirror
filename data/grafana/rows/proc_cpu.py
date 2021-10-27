{
    'process_cpu': {
        'stacked': True,
        'queries': {
            'cpu': {
                'filters': {
                    '_measurement': 'procstat',
                    '_field': [
                        'cpu_usage',
                    ],
                },
                'resolution': 6,
            },
        },
        'unit': 'percent',
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
