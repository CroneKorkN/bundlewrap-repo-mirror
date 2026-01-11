{
    'in': {
        'stacked': True,
        'queries': {
            'in': {
                'filters': {
                    '_measurement': 'mikrotik_interface_generic',
                    '_field': [
                        'in_ucast_pkts',
                        'in_mcast_pkts',
                        'in_bcast_pkts',
                    ],
                    'ifType': [6],
                    'operating_system': 'routeros',
                },
                'function': 'derivative',
                'over': 0,
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
                    '_measurement': 'mikrotik_interface_generic',
                    '_field': [
                        'out_ucast_pkts',
                        'out_mcast_pkts',
                        'out_bcast_pkts',
                    ],
                    'ifType': [6],
                    'operating_system': 'routeros',
                },
                'function': 'derivative',
                'over': 0,
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
