{
    'supergroups': [
        'debian',
    ],
    'metadata': {
        'apt': {
            'sources': {
                'deb https://deb.debian.org/debian {codename} main contrib non-free non-free-firmware',
                'deb https://deb.debian.org/debian {codename}-updates main contrib non-free non-free-firmware',
                'deb https://deb.debian.org/debian {codename}-backports main contrib non-free non-free-firmware',
                'deb https://security.debian.org/ {codename}-security main contrib non-free non-free-firmware',
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
