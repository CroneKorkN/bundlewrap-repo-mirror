defaults = {
    'apt': {
        'packages': {
            'linux-image-amd64': {
                'installed': False,
            },
            'proxmox-default-kernel': {},
            # after reboot
            'proxmox-ve': {},
            'postfix': {},
            'open-iscsi': {},
            'chrony': {},
            'os-prober': {
                'installed': False,
            },
            'dnsmasq-base': {},
        },
        'sources': {
            'proxmox-ve': {
                'options': {
                    'aarch': 'amd64',
                },
                'urls': {
                    'http://download.proxmox.com/debian/pve',
                },
                'suites': {
                    '{codename}',
                },
                'components': {
                    'pve-no-subscription',
                },
                'key': 'proxmox-ve-{codename}',
            },
        },
    },
    # 'nftables': {
    #     'input': {
    #         'tcp dport 8006 accept',
    #     },
    # },
    'zfs': {
        'datasets': {
            'tank/proxmox-ve': {
                'mountpoint': '/var/lib/proxmox-ve',
            },
        }
    }
}


# @metadata_reactor.provides(
#     'systemd',
# )
# def bridge(metadata):
#     return {
#         'systemd': {
#             'units': {
#                 # f'internal.network': {
#                 #     'Network': {
#                 #         'Bridge': 'br0',
#                 #     },
#                 # },
#                 'br0.netdev': {
#                     'NetDev': {
#                         'Name': 'br0',
#                         'Kind': 'bridge'
#                     },
#                 },
#                 'br0.network': {
#                     'Match': {
#                         'Name': 'br0',
#                     },
#                     'Network': {
#                         'Unmanaged': 'yes'
#                     },
#                 },
#             },
#         },
#     }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'has_websockets': True,
            'vhosts': {
                metadata.get('proxmox-ve/domain'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'https://localhost:8006',
                        'websockets': True,
                    }
                },
            },
        },
    }
