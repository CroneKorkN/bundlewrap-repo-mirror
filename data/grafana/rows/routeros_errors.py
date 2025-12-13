{
    'errors_in': {
        'stacked': False,
        'queries': {
            'errors_in': {
                'filters': {
                    '_measurement': 'interface',
                    '_field': ['in_errors'],
                    'operating_system': 'routeros',
                },
                'function': 'max',
                'derivative': True,
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
    'errors_out': {
        'stacked': False,
        'queries': {
            'errors_out': {
                'filters': {
                    '_measurement': 'interface',
                    '_field': ['out_errors'],
                    'operating_system': 'routeros',
                },
                'function': 'max',
                'derivative': True,
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
