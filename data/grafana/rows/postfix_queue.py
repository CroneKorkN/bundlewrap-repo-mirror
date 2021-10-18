{
    'length': {
        'stacked': True,
        'queries': {
            'length': {
                'filters': {
                    '_measurement': 'postfix_queue',
                    '_field': [
                        'length',
                    ],
                },
                'function': 'mean',
            },
        },
        'display_name': '__field.labels.queue'
    },
    'size': {
        'stacked': True,
        'queries': {
            'size': {
                'filters': {
                    '_measurement': 'postfix_queue',
                    '_field': [
                        'size',
                    ],
                },
                'function': 'mean',
            },
        },
        'display_name': '__field.labels.queue'
    },
    'age': {
        'stacked': True,
        'queries': {
            'age': {
                'filters': {
                    '_measurement': 'postfix_queue',
                    '_field': [
                        'age',
                    ],
                },
                'function': 'mean',
            },
        },
        'display_name': '__field.labels.queue'
    },
}
