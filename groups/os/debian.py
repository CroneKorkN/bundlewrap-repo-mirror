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
            'packages': {
                'mtr-tiny': {},
            },
            # https://ftp-master.debian.org/keys.html
        },
    },
    'os': 'debian',
    'pip_command': 'pip3',
}
