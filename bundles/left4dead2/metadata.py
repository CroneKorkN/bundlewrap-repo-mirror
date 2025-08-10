defaults = {
    'apt': {
        'packages': {
            'libc6_i386': {}, # installs libc6:i386
            'lib32z1': {},
            'unzip': {},
        },
    },
    'left4dead2': {
        'servers': {},
    },
    'nftables': {
        'input': {
            'udp dport { 27005, 27020 } accept',
        },
    },
}
