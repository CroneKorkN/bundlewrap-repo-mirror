from hashlib import sha3_256

defaults = {
    'apt': {
        'packages': {
            'icingadb': {},
            'icingadb-web': {},
            'icingaweb2': {},
            'icingadb-redis': {},
        },
        'sources': {
            'deb https://packages.icinga.com/debian icinga-{release} main',
            'deb https://packages.icinga.com/debian icinga-{release}-testing main',
        },
    },
    'postgresql': {
        'databases': {
            'icingadb': {
                'owner': 'icinga2',
            },
            'icingaweb2': {
                'owner': 'icingaweb2',
            },
        },
        'roles': {
            'icingadb': {
                'password': repo.vault.password_for(f'psql icinga2 on {node.name}'),
            },
            'icingaweb2': {
                'password': repo.vault.password_for(f'psql icingaweb2 on {node.name}'),
            },
        },
    },
    # 'zfs': {
    #     'datasets': {
    #         'tank/icinga2': {
    #             'mountpoint': '/var/lib/icingadb',
    #             'needed_by': {
    #                 'pkg_apt:icingadb',
    #                 'pkg_apt:icingadb-web',
    #                 'pkg_apt:icingaweb2',
    #             },
    #         },
    #     },
    # },
}

# 
# @metadata_reactor.provides(
#     'icingaweb2/setup_token',
# )
# def setup_token(metadata):
#     return {
#         'icingaweb2': {
#             'setup_token': sha3_256(metadata.get('id').encode()).hexdigest()[:16],
#         },
#     }
# 
# 
# @metadata_reactor.provides(
#     'nginx/vhosts',
# )
# def nginx(metadata):
#     return {
#         'nginx': {
#             'vhosts': {
#                 metadata.get('icinga2/hostname'): {
#                     'content': 'icingaweb2/vhost.conf',
#                     'context': {
#                     },
#                 },
#             },
#         },
#     }
