# https://teamvault.apps.seibert-media.net/secrets/mkqMRv/
# https://console.hetzner.cloud/projects/889138/servers/46578341

# mailman.ckn.li

{
    'hostname': '91.99.123.176',
    'groups': [
        'backup',
        'debian-12',
        'monitored',
        'webserver',
    ],
    'bundles': [
        'mailman',
        'wireguard',
        'zfs',
        'postgresql',
    ],
    'metadata': {
        'id': '854cb39f-d964-4cc7-9051-ba6574708820',
        'network': {
            'internal': {
                'interface': 'ens10',
                'ipv4': '10.0.229.2/24',
            },
            'external': {
                'interface': 'eth0',
                'ipv4': '91.99.123.176/32',
                'gateway4': '172.31.1.1',
                'ipv6': '2a01:4f8:c013:2030::2/64',
                'gateway6': 'fe80::1',
            },
        },
        'mailman': {
            'hostname': 'mailman.ckn.li',
            'site_owner_email': '!decrypt:encrypt$gAAAAABoWEeTyypfKw9l9jnNgF4GlS0-6O2NWCB0f3Fj1XnQ_HMjHXymAL8FWTyQjRmz3r8KnGJ-sogfnhW6lub_pnuk-wqB5Zuy9tgGsfi3RvkyNaOUeTE=',
            'dmarc_report_email': 'dmarc@sublimity.de',

            # 'smtp_host': 'smtp.ionos.de',
            # 'smtp_port': 465,
            # 'smtp_user': '!decrypt:encrypt$gAAAAABoWEcZlLxiTKluyg3gZ-un2fYkuviW9BD9tTW8mfKBL5d41Z1X7LtI5CDnhhLXTGFpPnY1thr17h22oW3Ybz_WPgvbJVepnVwmeQwvMpg2psATKAY=',
            # 'smtp_password': '!decrypt:encrypt$gAAAAABoWDusH3XY4ONh8MnmfBbyHW477ipjSycb3TiDGXxO5eujum80zXjNrOblswCGRTHsW9UasM_dXeeGBsa7KcK4s6AK_eynXCWeLCtXfrUSE_oEd7c='
        },
        'systemd_timers': {
            'cron': {
                'enabled': True,
            },
        },
        'vm': {
            'cores': 2,
            'ram': 4096,
        },
        'wireguard': {
            'my_ip': '172.30.0.240/32',
            's2s': {
                'htz.mails': {
                    'allowed_ips': [
                        '10.0.0.0/24',
                        '10.0.2.0/24',
                        '10.0.9.0/24',
                        '10.0.10.0/24',
                    ],
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'devices': [
                        '/var/lib/zfs_file',
                    ],
                },
            },
        },
    },
}
