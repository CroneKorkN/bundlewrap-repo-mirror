from hashlib import sha256


defaults = {
    'apt': {
        'packages': {
            'iperf3': {},
            'iperf': {
                'installed': False,
            },
        }
    },
    # 'iperf3': {
    #     'username': node.name,
    #     'password': repo.vault.password_for(f'{node.name} iperf3').value,
    #     'authorized_users': {},
    # },
    'nftables': {
        'input': {
            'tcp dport 5202 ip saddr { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 } accept',
            'udp dport 5202 ip saddr { 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 } accept',
        },
    },
    'systemd': {
        'units': {
            'iperf3.service': {
                'Unit': {
                    'Description': 'iperf3 server',
                    'After': {
                        'syslog.target',
                        'network.target',
                    },
                },
                'Service': {
                    # 'ExecStart': '/usr/bin/iperf3 --server --port 5202 --authorized-users-path /etc/iperf3/authorized_users',
                    'ExecStart': '/usr/bin/iperf3 --server --port 5202',
                },
                'Install': {
                    'WantedBy': {
                        'multi-user.target',
                    },
                },
            },
        },
        'services': {
            'iperf3.service': {},
        },
    },
}


# @metadata_reactor.provides(
#     'iperf3/hash',
# )
# def hash(metadata):
#     username, password = metadata.get('iperf3/username'), metadata.get('iperf3/password')

#     return {
#         'iperf3': {
#             'hash': sha256(f'{{{username}}}{password}'.encode()).hexdigest(),
#         },
#     }


# @metadata_reactor.provides(
#     'iperf3/authorized_users',
# )
# def iperf3(metadata):
#     return {
#         'iperf3': {
#             'authorized_users': set(
#                 f"{other_node.metadata.get('iperf3/username')},{other_node.metadata.get('iperf3/hash')}"
#                     for other_node in repo.nodes
#                     if other_node.has_bundle('iperf3')
#             ),
#         },
#     }
