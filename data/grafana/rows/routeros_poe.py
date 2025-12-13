{
    'power': {
        'stacked': True,
        'queries': {
            'power': {
                'filters': {
                    '_measurement': 'poe',
                    '_field': ['power'],
                    'operating_system': 'routeros',
                },
                'function': 'mean',
                'multiply': 0.1,
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'watt',
        'tooltip': 'multi',
        'display_name': '${__field.labels.ifName} - ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'current': {
        'stacked': True,
        'queries': {
            'voltage': {
                'filters': {
                    '_measurement': 'poe',
                    '_field': ['current'],
                    'operating_system': 'routeros',
                },
                'function': 'mean',
                'multiply': 0.1,
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'ampere',
        'tooltip': 'multi',
        'display_name': '${__field.labels.ifName} - ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'voltage': {
        'stacked': False,
        'queries': {
            'voltage': {
                'filters': {
                    '_measurement': 'poe',
                    '_field': ['voltage'],
                    'operating_system': 'routeros',
                },
                'function': 'mean',
                'multiply': 0.1,
                'over': 0,
            },
        },
        'min': 0,
        'unit': 'volt',
        'tooltip': 'multi',
        'display_name': '${__field.labels.ifName} - ${__field.labels.ifAlias}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
