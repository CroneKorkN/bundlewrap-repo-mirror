defaults = {
    'apt': {
        'packages': {
            'nftables': {},
        },
    },
    'nftables': {
        'input': {
            'tcp dport 22 accept',
        },
        'forward': {},
        'nat': {},
        'output': {},
    },
}
