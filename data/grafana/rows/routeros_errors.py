{
    'in': {
        'stacked': True,
        'queries': {
            'in': {
                'filters': {
                    '_measurement': 'interface',
                    '_field': ['in_errors'],
                    'operating_system': 'routeros',
                },
                'function': 'derivative',
            },
        },
        'min': 0,
        'unit': 'pps',
        'tooltip': 'multi',
        'display_name': '${__field.labels.ifName} - ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'out': {
        'stacked': True,
        'queries': {
            'out': {
                'filters': {
                    '_measurement': 'interface',
                    '_field': ['out_errors'],
                    'operating_system': 'routeros',
                },
                'function': 'derivative',
            },
        },
        'min': 0,
        'unit': 'pps',
        'tooltip': 'multi',
        'display_name': '${__field.labels.ifName} - ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
