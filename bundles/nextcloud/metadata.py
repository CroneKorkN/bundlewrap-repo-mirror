import string
from uuid import UUID

defaults = {
    'apt': {
        'packages': {
            'php': {},
            'php-curl': {},
            'php-gd': {},
            'php-json': {},
            'php-xml': {},
            'php-mbstring': {},
            'php-cli': {},
            'php-cgi': {},
            'php-zip': {},
        },
    },
    'archive': {
        'paths': {
            '/var/lib/nextcloud': {
                'exclude': [
                    '^appdata_',
                    '^updater-',
                    '^nextcloud\.log',
                    '^updater\.log',
                    '^[^/]+/cache',
                    '^[^/]+/files_versions',
                    '^[^/]+/files_trashbin',
                ],
            },
        },
    },
    'backup': {
        'paths': [
            '/etc/nextcloud/config.php',
        ],
    },
    'nextcloud': {
        'admin_user': 'admin',
        'admin_pass': repo.vault.password_for(f'{node.name} nextcloud admin pw'),
    },
    'postgresql': {
        'roles': {
            'nextcloud': {
                'password': repo.vault.password_for(f'{node.name} nextcloud db pw'),
            },
        },
        'databases': {
            'nextcloud': {
                'owner': 'nextcloud',
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/nextcloud': {
                'mountpoint': '/var/lib/nextcloud',
                'needed_by': [
                    'bundle:nextcloud',
                ],
            },
        },
    },
}

# @metadata_reactor.provides(
#     'nginx/vhosts/nextcloud/domain',
# )
# def nginx(metadata):
#     return {
#         'nginx': {
#             'vhosts': {
#                 'nextcloud': {
#                     'domain': metadata.get('nextcloud/domain'),
#                     'webroot': '/opt/nextcloud',
#                     'php': True,
#                 },
#             },
#         },
#     }
