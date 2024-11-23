defaults = {
    'backups': {
        'paths': {
            '/opt/n8n',
        },
    },
    'users': {
        'n8n': {
            'home': '/opt/n8n',
        },
    },
    'postgresql': {
        'databases': {
            'n8n': {
                'when_creating': {
                    'encoding': 'UTF8',
                    'collation': 'C.UTF-8',
                    'ctype': 'C.UTF-8',
                },
            },
        },
        'roles': {
            'n8n': {
                'password': repo.vault.password_for(f'{node.name} n8n psql'),
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/n8n': {
                'compression': 'on',
                'mountpoint': '/opt/n8n',
                'needed_by': {'directory:/opt/n8n'},
            },
        },
    },
}


@metadata_reactor.provides(
    'icinga2_api/n8n/services/N8N UPDATE',
)
def icinga_check_for_new_release(metadata):
    return {
        'icinga2_api': {
            'n8n': {
                'services': {
                    'N8N UPDATE': {
                        'command_on_monitored_host':
                            f'/usr/local/share/icinga/plugins/check_github_for_new_release '
                            f'--repo n8n-io/n8n --current-version n8n@{metadata.get("n8n/version")}',
                        'check_interval': '60m',
                    },
                },
            },
        },
    }


@metadata_reactor.provides(
    'systemd/services/n8n',
)
def systemd(metadata):
    return {
        'systemd': {
            'services': {
                'n8n': {
                    'content': {
                        'Unit': {
                            'Description': 'n8n',
                            'Requires': 'network.target postgresql.service',
                            'After': 'postgresql.service',
                        },
                        'Service': {
                            'Restart': 'always',
                            'RestartSec': '5',
                            'WorkingDirectory': '/opt/n8n',
                            'ExecStart': '/usr/bin/npx n8n start',
                            'User': 'n8n',
                            'Group': 'n8n',
                        },
                    },
                    'env_as_file': metadata.get('n8n/env'),
                    'needs': {
                        'action:install_n8n',
                    },
                },
            },
        },
    }
