from shlex import quote


defaults = {
    'apt': {
        'packages': {
            'php': {},
            'php-redis': {},
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
            'php-intl': {},
            'php-imagick': {},
            'libmagickcore-6.q16-6-extra': {},
            'php-gmp': {},
            'php-bcmath': {},
        },
    },
    'archive': {
        'paths': {
            '/var/lib/nextcloud': {
                'exclude': [
                    '^appdata_',
                    '^updater-',
                    '^nextcloud\\.log',
                    '^updater\\.log',
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
        'admin_pass': repo.vault.password_for(f'{node.name} nextcloud admin pw').value,
        'config': {},
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
                'password': repo.vault.password_for(f'{node.name} nextcloud db pw').value,
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
            'kill_mode': 'process',
        },
        'nextcloud-scan-app-data': {
            'command': '/usr/bin/php /opt/nextcloud/occ files:scan-app-data',
            'when': 'yearly',
            'user': 'www-data',
        },
        'nextcloud-scan-files': {
            'command': '/usr/bin/php /opt/nextcloud/occ files:scan --all',
            'when': 'weekly',
            'user': 'www-data',
            'after': {
                'nextcloud-scan-app-data.service',
            },
        },
        'nextcloud-generate-all-previews': {
            'command': '/bin/bash -c ' + quote('php /opt/nextcloud/occ preview:generate-all --workers="$(nproc)" --no-interaction -vvv'),
            'when': 'monthly',
            'user': 'www-data',
            'after': {
                'nextcloud-scan-files.service',
            },
        },
        'nextcloud-generate-new-previews': {
            'command': '/usr/bin/php /opt/nextcloud/occ preview:pre-generate',
            'when': '*:0/5', # every 5 minutes
            'user': 'www-data',
            'after': {
                'nextcloud-generate-all-previews.service',
            },
        },
    },
}


@metadata_reactor.provides(
    'nextcloud/config',
)
def config(metadata):
    return {
        'nextcloud': {
            'config': {
                'dbuser': 'nextcloud',
                'dbpassword': metadata.get('postgresql/roles/nextcloud/password'),
                'dbname': 'nextcloud',
                'dbhost': 'localhost',
                'dbtype': 'pgsql',
                'dbtableprefix': 'oc_',
                'datadirectory': '/var/lib/nextcloud',
                'dbport': '5432',
                'apps_paths': [
                    {
                        'path': '/opt/nextcloud/apps',
                        'url': '/apps',
                        'writable': False
                    },
                    {
                        'path': '/var/lib/nextcloud/.userapps',
                        'url': '/userapps',
                        'writable': True
                    }
                ],
                'cache_path': '/var/lib/nextcloud/.cache',
                'upgrade.disable-web': True,
                'memcache.local': '\\OC\\Memcache\\Redis',
                'memcache.locking': '\\OC\\Memcache\\Redis',
                'memcache.distributed': '\\OC\\Memcache\\Redis',
                'redis': {
                    'host': '/var/run/redis/nextcloud.sock'
                },
                'trusted_domains': [
                    'localhost',
                    '127.0.0.1',
                    metadata.get('nextcloud/hostname'),
                ],
                'enabledPreviewProviders': [
                    'OC\\Preview\\Image',
                    'OC\\Preview\\Movie',
                    'OC\\Preview\\HEIC',
                ],
                'preview_max_x': 1920,
                'preview_max_y': 1920,
                'preview_max_scale_factor': 4,
                'log_type': 'syslog',
                'syslog_tag': 'nextcloud',
                'logfile': '',
                'loglevel': 2,
                'default_phone_region': 'DE',
                'versions_retention_obligation': 'auto, 90',
                'simpleSignUpLink.shown': False,
                'allow_local_remote_servers': True, # FIXME?
                'maintenance_window_start': 1, # https://docs.nextcloud.com/server/29/admin_manual/configuration_server/background_jobs_configuration.html#maintenance-window-start
            },
        },
    }


@metadata_reactor.provides(
    'zfs/datasets',
)
def zfs(metadata):
    return {
        'zfs': {
            'datasets': {
                f"{metadata.get('zfs/storage_classes/hdd')}/nextcloud": {
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
