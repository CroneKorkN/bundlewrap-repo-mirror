{
    'hostname': '10.0.0.190',
    'groups': [
        'autologin',
        'debian-12',
        'hardware',
        'home',
        'monitored',
        'webserver',
    ],
    'bundles': [
        'wireguard',
    ],
    'metadata': {
        'id': '4eb7ba69-37fa-4594-8d54-3ebfc4e7e5d6',
        'network': {
            'internal': {
                'interface': 'eth0',
                'ipv4': '10.0.0.190/24',
                'gateway4': '10.0.0.1',
            },
        },
        'apt': {
            'packages': {
                'alsa-utils': {},
                'espeak': {},
                'libnginx-mod-http-lua': {},
            },
        },
        'nginx': {
            'vhosts': {
                'rufbereitschaftsalarm.ckn.li': {
                    'content': 'nginx/run_program.conf',
                    'context': {
                        'script': 'hello',
                    },
                },
            },
        },
        'systemd': {
            'units': {
                "wireguard.network": {
                    "Route#smedia": {
                        "Destination": "10.200.128.1",
                        "Gateway": "10.200.128.11"
                    },
                },
                "wireguard.netdev": {
                    "NetDev": {
                        "Description": "WireGuard server",
                        "Kind": "wireguard",
                        "Name": "wg0"
                    },
                    "WireGuard": {
                        "ListenPort": 51820,
                        "PrivateKey": "encrypt$gAAAAABk6FEX92wQzlBIqxP6w5FQydlrDqOZeo1AZS9zaBE3QzujtBnB_cf6KlECzmoljr71dmRiFN5yvA8bzRIpcecvnufIji1XNg-i1UW1fq393XppRq0p9EtNBVzoXoyzZFEcjQRo"
                    },
                    "WireGuardPeer#rufbereitsschaftsalarm": {
                        "AllowedIPs": "0.0.0.0/0",
                        "Endpoint": "185.122.180.82:51820",
                        "PersistentKeepalive": 30,
                        "PresharedKey": "!decrypt:encrypt$gAAAAABk6FD0_39AzxKTTse3ukqs7VOcZ5mPsBsN09Y4FgITOEnbBVWZ-zDsaZi-woNbp4k10nrJtIrqz8a-FIFdNbQaTgulhRDKF6TFH4BhYlEB7d8NH5CU3kTTtqtjSWW9GPqAgb3z",
                        "PublicKey": "gPKjFV8mAx5GZdfPmjThNolpSaXs285e7YznhaBlOwY="
                    }
                },
            },
        },
        'wireguard': {
            'my_ip': '10.200.128.11/24',
        },
    },
}
