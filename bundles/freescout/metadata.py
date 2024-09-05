from base64 import b64decode

# hash: SCRAM-SHA-256$4096:tQNfqQi7seqNDwJdHqCHbg==$r3ibECluHJaY6VRwpvPqrtCjgrEK7lAkgtUO8/tllTU=:+eeo4M0L2SowfyHFxT2FRqGzezve4ZOEocSIo11DATA=
database_password = repo.vault.password_for(f'{node.name} postgresql freescout').value

defaults = {
    'apt': {
        'packages': {
            'git': {},
            'php': {},
            'php-pgsql': {},
            'php-fpm': {},
            'php-mbstring': {},
            'php-xml': {},
            'php-imap': {},
            'php-zip': {},
            'php-gd': {},
            'php-curl': {},
            'php-intl': {},
        },
    },
    'freescout': {
        'env': {
            'APP_TIMEZONE': 'Europe/Berlin',
            'DB_CONNECTION': 'pgsql',
            'DB_HOST': '127.0.0.1',
            'DB_PORT': '5432',
            'DB_DATABASE': 'freescout',
            'DB_USERNAME': 'freescout',
            'DB_PASSWORD': database_password,
            'APP_KEY': 'base64:' + repo.vault.random_bytes_as_base64_for(f'{node.name} freescout APP_KEY', length=32).value
        },
    },
    'php': {
        'php.ini': {
            'cgi': {
                'fix_pathinfo': '0',
            },
        },
    },
    'postgresql': {
        'roles': {
            'freescout': {
                'password_hash': repo.libs.postgres.generate_scram_sha_256(
                    database_password,
                    b64decode(repo.vault.random_bytes_as_base64_for(f'{node.name} postgres freescout', length=16).value.encode()),
                ),
            },
        },
        'databases': {
            'freescout': {
                'owner': 'freescout',
            },
        },
    },
    # 'systemd': {
    #     'units': {
    #         f'freescout-cron.service': {
    #             'Unit': {
    #                 'Description': 'Freescout Cron',
    #                 'After': 'network.target',
    #             },
    #             'Service': {
    #                 'User': 'www-data',
    #                 'Nice': 10,
    #                 'ExecStart': f"/usr/bin/php /opt/freescout/artisan schedule:run"
    #             },
    #             'Install': {
    #                 'WantedBy': {
    #                     'multi-user.target'
    #                 }
    #             },
    #         }
    #     },
    # },
    'systemd-timers': {
        'freescout-cron': {
            'command': '/usr/bin/php /opt/freescout/artisan schedule:run',
            'when': '*-*-* *:*:00',
            'RuntimeMaxSec': '180',
            'user': 'www-data',
        },
    },
    'zfs': {
        'datasets': {
            'tank/freescout': {
                'mountpoint': '/opt/freescout',
            },
        },
    },
}




@metadata_reactor.provides(
    'freescout/env/APP_URL',
)
def freescout(metadata):
    return {
        'freescout': {
            'env': {
                'APP_URL': 'https://' + metadata.get('freescout/domain') + '/',
            },
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('freescout/domain'): {
                    'content': 'freescout/vhost.conf',
                },
            },
        },
    }
