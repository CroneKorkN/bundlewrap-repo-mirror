import string
from uuid import UUID

defaults = {
    'apt': {
        'packages': {
            'php': {},
            'php-fpm': {},
            'php-curl': {},
            'php-gd': {},
            'php-json': {},
            'php-xml': {},
            'php-mbstring': {},
            'php-cli': {},
            'php-cgi': {},
            'php-zip': {},
            'php-pgsql': {},
            'php-bz2': {}, # face recognition
        },
        'sources': {
            'deb https://repo.delellis.com.ar {release} {release}', # face recognition
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
        'paths': {
            '/etc/nextcloud/config.php',
        },
    },
    'nextcloud': {
        'admin_user': 'admin',
        'admin_pass': repo.vault.password_for(f'{node.name} nextcloud admin pw'),
    },
    'php': {
        'post_max_size': '32G',
        'www.conf': {
            'env[HOSTNAME]': '$HOSTNAME',
            'env[PATH]': '/usr/local/bin:/usr/bin:/bin',
            'env[TMP]': '/tmp',
            'env[TMPDIR]': '/tmp',
            'env[TEMP]': '/tmp',
        },
        'php.ini': {
            'PHP': {
                'memory_limit': '3G', # face recognition requires 2G
            },
        },
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
    'redis': {
        'nextcloud': {},
    },
    'systemd-timers': {
        'nextcloud-cron': {
            'command': '/usr/bin/php -f /opt/nextcloud/cron.php',
            'when': '*:0/5',
            'user': 'www-data',
        },
        'nextcloud-rescan': {
            'command': '/opt/nextcloud_rescan',
            'when': 'Sun 00:00:00',
            'user': 'www-data',
        },
        'nextcloud-face-recognition': {
            'command': '/usr/bin/php -f /opt/nextcloud/occ face:background_job -t 1800',
            'when': '*:0/10',
            'user': 'www-data',
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


@metadata_reactor.provides(
    'nginx/vhosts'
)
def vhost(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('nextcloud/hostname'): {
                    'content': 'nextcloud/vhost.conf',
                    'context': {
                        'root': '/opt/nextcloud',
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts'
)
def pdlib(metadata):
    return {
        'apt': {
            'packages': {
                f"php{metadata.get('php/version')}-pdlib": {},
            },
        },
    }
