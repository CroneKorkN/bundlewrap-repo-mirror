database_password = repo.vault.password_for(f'{node.name} postgresql gitea').value

defaults = {
    'apt': {
        'packages': {
            'git': {
                'needed_by': {
                    'svc_systemd:gitea',
                }
            },
        },
    },
    'gitea': {
        'conf': {
            'DEFAULT': {
                'WORK_PATH': '/var/lib/gitea',
            },
            'database': {
                'DB_TYPE': 'postgres',
                'HOST': 'localhost:5432',
                'NAME': 'gitea',
                'USER': 'gitea',
                'PASSWD': database_password,
                'SSL_MODE': 'disable',
                'LOG_SQL': 'false',
            },
        },
    },
    'postgresql': {
        'roles': {
            'gitea': {
                'password': database_password,
            },
        },
        'databases': {
            'gitea': {
                'owner': 'gitea',
            },
        },
    },
    'systemd': {
        'units': {
            'gitea.service': {
                'Unit': {
                    'Description': 'gitea',
                    'After': {'syslog.target', 'network.target'},
                    'Requires': 'postgresql.service',
                },
                'Service': {
                    'RestartSec': '2s',
                    'Type': 'simple',
                    'User': 'git',
                    'Group': 'git',
                    'WorkingDirectory': '/var/lib/gitea/',
                    'ExecStart': '/usr/local/bin/gitea web -c /etc/gitea/app.ini',
                    'Restart': 'always',
                    'Environment': 'USER=git HOME=/home/git GITEA_WORK_DIR=/var/lib/gitea',
                },
                'Install': {
                    'WantedBy': {'multi-user.target'},
                },
            },
        },
    },
    'users': {
        'git': {
            'home': '/home/git',
        },
    },
    'zfs': {
        'datasets': {
            'tank/gitea': {
                'mountpoint': '/var/lib/gitea',
            },
        },
    },
}


@metadata_reactor.provides(
    'gitea/conf',
)
def conf(metadata):
    domain = metadata.get('gitea/domain')

    return {
        'gitea': {
            'conf': {
                'server': {
                    'SSH_DOMAIN': domain,
                    'DOMAIN': domain,
                    'ROOT_URL': f'https://{domain}/',
                    'LFS_JWT_SECRET': repo.vault.password_for(f'{node.name} gitea lfs_secret_key', length=43),
                },
                'security': {
                    'INTERNAL_TOKEN': repo.vault.password_for(f'{node.name} gitea internal_token'),
                    'SECRET_KEY': repo.vault.password_for(f'{node.name} gitea security_secret_key'),
                },
                'service': {
                    'NO_REPLY_ADDRESS': f'noreply.{domain}',
                },
                'oauth2': {
                    'JWT_SECRET': repo.vault.password_for(f'{node.name} gitea oauth_secret_key', length=43),
                },
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
                metadata.get('gitea/domain'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:3500',
                    }
                },
            },
        },
    }
