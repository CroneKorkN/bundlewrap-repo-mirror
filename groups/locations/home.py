{
    'metadata': {
        # resolve via the local router first, so dns keeps working without the vpn to htz
        'overwrite_nameservers': [
            '10.0.0.1',
            '10.0.10.2',
        ],
        'nftables': {
            'input': {
                'udp dport 161 accept',
            },
        },
    },
}
