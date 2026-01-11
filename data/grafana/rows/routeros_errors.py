{
    'critical': {
        'stacked': True,
        'queries': {
            'generic': {
                'filters': {
                    '_measurement': 'mikrotik_interface_generic',
                    '_field': [
                        'in_errors',
                        'out_errors',
                    ],
                    'operating_system': 'routeros',
                },
                'function': 'difference',
                'over': 0,
            },
            'mikrotik': {
                'filters': {
                    '_measurement': 'mikrotik_interface_detailed',
                    '_field': [
                        'rx_fcs_errors',
                        'rx_align_errors',
                        'rx_code_errors',
                        'rx_carrier_errors',
                        'rx_jabber',
                        'rx_fragment',
                        'rx_length_errors',
                        'tx_late_collisions',
                        'tx_excessive_collisions',
                        'link_downs',
                    ],
                    'operating_system': 'routeros',
                },
                'function': 'difference',
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'cps',
        'tooltip': 'multi',
        'display_name': '${__field.name} ${__field.labels.ifName} ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'table',
            'placement': 'right',
            'calcs': [
                'max',
            ],
        },
    },
    'warning': {
        'stacked': True,
        'queries': {
            'generic': {
                'filters': {
                    '_measurement': 'mikrotik_interface_generic',
                    '_field': [
                        'in_discards',
                        'out_discards',
                    ],
                    'operating_system': 'routeros',
                },
                'function': 'difference',
                'over': 0,
            },
            'mikrotik': {
                'filters': {
                    '_measurement': 'mikrotik_interface_detailed',
                    '_field': [
                        'rx_too_short',
                        'rx_too_long',
                        'rx_drop',
                        'tx_drop',
                        'rx_pause',
                        'tx_pause',
                        'tx_pause_honored',
                        'tx_collisions',
                        'tx_total_collisions',
                    ],
                    'operating_system': 'routeros',
                },
                'function': 'difference',
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'cps',
        'tooltip': 'multi',
        'display_name': '${__field.name} ${__field.labels.ifName} ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'table',
            'placement': 'right',
            'calcs': [
                'max',
            ],
        },
    },
}
