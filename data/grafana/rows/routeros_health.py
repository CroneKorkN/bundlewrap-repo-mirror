{
    'temperature': {
        'stacked': False,
        'queries': {
            'temp': {
                'filters': {
                    '_measurement': 'mikrotik_health',
                    'sensor': [
                        'temperature',
                        'cpu-temperature',
                        'switch-temperature',
                        'board-temperature1',
                        'sfp-temperature',
                    ],
                    '_field': [
                        'value',
                    ],
                    'operating_system': 'routeros',
                },
            },
        },
        'min': 0,
        'unit': 'celsius',
        'tooltip': 'multi',
        'display_name': '${__field.labels.sensor}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'fan': {
        'stacked': False,
        'queries': {
            'temp': {
                'filters': {
                    '_measurement': 'mikrotik_health',
                    'sensor': [
                        'fan1-speed',
                        'fan2-speed',
                    ],
                    '_field': [
                        'value',
                    ],
                    'operating_system': 'routeros',
                },
            },
        },
        'min': 0,
        'unit': 'rpm',
        'tooltip': 'multi',
        'display_name': '${__field.labels.sensor}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'psu_current': {
        'stacked': False,
        'queries': {
            'temp': {
                'filters': {
                    '_measurement': 'mikrotik_health',
                    'sensor': [
                        'psu1-current',
                        'psu2-current',
                    ],
                    '_field': [
                        'value',
                    ],
                    'operating_system': 'routeros',
                },
                'multiply': 0.1,
            },
        },
        'min': 0,
        'unit': 'ampere',
        'tooltip': 'multi',
        'display_name': '${__field.labels.sensor}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'psu_voltage': {
        'stacked': False,
        'queries': {
            'temp': {
                'filters': {
                    '_measurement': 'hw',
                    'sensor': [
                        'psu1-voltage',
                        'psu2-voltage',
                    ],
                    '_field': [
                        'value',
                    ],
                    'operating_system': 'routeros',
                },
                'multiply': 0.1,
            },
        },
        'min': 0,
        'unit': 'volt',
        'tooltip': 'multi',
        'display_name': '${__field.labels.sensor}',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
