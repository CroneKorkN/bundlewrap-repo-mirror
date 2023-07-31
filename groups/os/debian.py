{
    'supergroups': [
        'linux',
    ],
    'bundles': [
        'apt',
        'nftables',
        'pip',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'debian': {
                    'types': {'deb'},
                    'url': 'https://deb.debian.org/debian',
                    'distributions': {
                        '{codename}',
                        '{codename}-security',
                        '{codename}-updates',
                    },
                    'components': {
                        'main',
                        'contrib',
                        'non-free',
                        'non-free-firmware',
                    },
                    'key': 'debian',
                },
            },
            'packages': {
                'mtr-tiny': {},
            },
            # https://ftp-master.debian.org/keys.html
        },
    },
    'os': 'debian',
    'pip_command': 'pip3',
}
