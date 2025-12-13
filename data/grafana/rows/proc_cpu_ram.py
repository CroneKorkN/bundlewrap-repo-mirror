{
    'cpu': {
        'stacked': True,
        'queries': {
            'cpu': {
                'filters': {
                    '_measurement': 'procstat',
                    '_field': [
                        'cpu_usage',
                    ],
                },
                'over': 0.2,
            },
        },
        'unit': 'percent',
        'display_name': '${__field.labels.process_name}',
        'legend': {
            'displayMode': 'table',
            'placement': 'right',
            'calcs': [
                'last',
            ],
        },
    },
    'ram': {
        'stacked': True,
        'queries': {
            'ram': {
                'filters': {
                    '_measurement': 'procstat',
                    '_field': [
                        'memory_rss',
                    ],
                },
                'over': 10*(10**6),
            },
        },
        'unit': 'bytes',
        'display_name': '${__field.labels.process_name}',
        'legend': {
            'displayMode': 'table',
            'placement': 'right',
            'calcs': [
                'last',
            ],
        },
    },
}
