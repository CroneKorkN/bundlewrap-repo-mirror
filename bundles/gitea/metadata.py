database_password = repo.vault.password_for(f'{node.name} postgresql gitea')

defaults = {
    'gitea': {
        'database': {
            'host': 'localhost',
            'port': '5432',
            'username': 'gitea',
            'password': database_password,
            'database': 'gitea',
        },
        'app_name': 'Gitea',
        'lfs_secret_key': repo.vault.password_for(f'{node.name} gitea lfs_secret_key', length=43),
        'security_secret_key': repo.vault.password_for(f'{node.name} gitea security_secret_key'),
        'oauth_secret_key': repo.vault.password_for(f'{node.name} gitea oauth_secret_key', length=43),
        'internal_token': repo.vault.password_for(f'{node.name} gitea internal_token'),
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
        'services': {
            'gitea': {
                'content': {
                    'Unit': {
                        'Description': 'gitea',
                        'After': 'syslog.target',
                        'After': 'network.target',
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
                        'WantedBy': 'multi-user.target',
                    },
                },
                'needs': [
                    'action:chmod_gitea',
                    'download:/usr/local/bin/gitea',
                    'file:/etc/systemd/system/gitea.service',
                    'file:/etc/gitea/app.ini',
                ],
            },
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
    'nginx/vhosts',
)
def nginx(metadata):
    if not node.has_bundle('nginx'):
        raise DoNotRunAgain

    return {
        'nginx': {
            'vhosts': {
                metadata.get('gitea/domain'): {
                    'proxy': {
                        '/': {
                            'target': 'http://127.0.0.1:22000',
                        },
                    },
                    'website_check_path': '/user/login',
                    'website_check_string': 'Sign In',
                },
            },
        },
    }
