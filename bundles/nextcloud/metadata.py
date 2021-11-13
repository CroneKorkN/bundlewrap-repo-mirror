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
            'env[hostname]': '$HOSTNAME',
            'env[path]': '/usr/local/bin:/usr/bin:/bin',
            'env[tmp]': '/tmp',
            'env[tmpdir]': '/tmp',
            'env[temp]': '/tmp',
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
            'command': '/usr/bin/sudo -u www-data /usr/bin/php -f /opt/nextcloud/cron.php',
            'when': '*:0/5',
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
