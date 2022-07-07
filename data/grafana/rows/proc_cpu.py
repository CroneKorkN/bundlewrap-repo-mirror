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
                'minimum': 1,
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
