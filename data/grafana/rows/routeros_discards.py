{
    'discards_in': {
        'stacked': False,
        'queries': {
            'discards_in': {
                'filters': {
                    '_measurement': 'interface',
                    '_field': ['in_discards'],
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
    'discards_out': {
        'stacked': False,
        'queries': {
            'discards_out': {
                'filters': {
                    '_measurement': 'interface',
                    '_field': ['out_discards'],
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
