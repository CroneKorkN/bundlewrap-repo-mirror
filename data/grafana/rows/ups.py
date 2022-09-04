{
    'charge': {
        'queries': {
            'charge': {
                'filters': {
                    '_measurement': 'apcupsd',
                    '_field': [
                        'BCHARGE',
                    ],
                },
                'function': 'mean',
            },
        },
        'max': 100,
        'min': 0,
        'unit': 'percent',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'load': {
        'queries': {
            'load': {
                'filters': {
                    '_measurement': 'apcupsd',
                    '_field': [
                        'LOADPCT',
                    ],
                },
                'function': 'mean',
            },
        },
        'min': 0,
        'unit': 'watts',
        'legend': {
            'displayMode': 'hidden',
        },
    },
    'time': {
        'queries': {
            'time': {
                'filters': {
                    '_measurement': 'apcupsd',
                    '_field': [
                        'TIMELEFT',
                    ],
                },
                'function': 'mean',
            },
        },
        'min': 0,
        'unit': 'minutes',
        'legend': {
            'displayMode': 'hidden',
        },
    },
}
