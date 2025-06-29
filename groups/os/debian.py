# https://ftp-master.debian.org/keys.html

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
                    'urls': {
                        'https://deb.debian.org/debian',
                    },
                    'suites': {
                        '{codename}',
                        '{codename}-updates',
                        '{codename}-backports',
                    },
                    'components': {
                        'main',
                        'contrib',
                        'non-free',
                    },
                    'key': 'debian-{version}',
                },
                'debian-security': {
                    'urls': {
                        'https://security.debian.org/',
                    },
                    'suites': {
                        '{codename}-security',
                    },
                    'components': {
                        'main',
                        'contrib',
                        'non-free',
                    },
                    'key': 'debian-{version}-security',
                },
            },
            'packages': {
                'mtr-tiny': {},
            },
        },
        # iperf3
        'nftables': {
            'input': {
                'tcp dport 5201 accept',
                'udp dport 5201 accept',
            },
        },

    },
    'os': 'debian',
    'pip_command': 'pip3',
}
