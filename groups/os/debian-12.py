{
    'supergroups': [
        'debian',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'debian': {
                    'components': {
                        'non-free-firmware',
                    },
                    'key': 'debian-12',
                },
                'debian-security': {
                    'components': {
                        'non-free-firmware',
                    },
                    'key': 'debian-12-security',
                },
            },
        },
        'php': {
            'version': '8.2',
        },
        'postgresql': {
            'version': '15',
        },
        'os_codename': 'bookworm',
    },
    'os_version': (12,),
}
