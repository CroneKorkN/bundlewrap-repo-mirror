defaults = {
    'apt': {
        'packages': {
            'kea-dhcp4-server': {},
        },
    },
    'kea': {
        'Dhcp4': {
            'interfaces-config': {
                'interfaces': [],
            },
            'lease-database': {
                'type': 'memfile',
                'lfc-interval': 3600
            },
            'subnet4': [],
            'loggers': [
                {
                    'name': 'kea-dhcp4',
                    'output_options': [
                        {
                            'output': 'syslog',
                        }
                    ],
                    'severity': 'INFO',
                },
            ],
        },
    },
}


@metadata_reactor.provides(

)
def subnets(metadata):
    pass
