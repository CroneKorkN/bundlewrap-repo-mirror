{
    'in': {
        'stacked': True,
        'queries': {
            'in': {
                'filters': {
                    '_measurement': 'mikrotik_interface_generic',
                    '_field': ['in_octets'],
                    'ifType': [6],
                    'operating_system': 'routeros',
                },
                'function': 'derivative',
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'bps',
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
                    '_measurement': 'mikrotik_interface_generic',
                    '_field': ['out_octets'],
                    'ifType': [6],
                    'operating_system': 'routeros',
                },
                'function': 'derivative',
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'bps',
        'tooltip': 'multi',
        'display_name': '${__field.labels.ifName} - ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
