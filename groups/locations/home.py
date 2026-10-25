{
    'metadata': {
        # resolve via the local router first, so dns keeps working without the vpn to htz
        'overwrite_nameservers': [
            '10.0.0.1',
            '172.30.0.1',
            '172.30.0.3',
        ],
        'nftables': {
            'input': {
                'udp dport 161 accept',
            },
        },
    },
}
