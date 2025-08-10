{
    'supergroups': [
        'debian',
        'debian-13-common',
    ],
    'bundles': [
        'systemd-networkd',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'debian': {
                    'components': {
                        'non-free-firmware',
                    },
                },
                'debian-security': {
                    'components': {
                        'non-free-firmware',
                    },
                },
            },
        },
        'php': {
            'version': '8.4',
        },
        'postgresql': {
            'version': '17',
        },
        'os_codename': 'trixie',
    },
    'os_version': (13,),
}
