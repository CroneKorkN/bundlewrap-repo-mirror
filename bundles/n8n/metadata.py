database_password = repo.vault.password_for(f'{node.name} postgresql n8n')

defaults = {
    'backups': {
        'paths': {
            '/opt/n8n',
        },
    },
    'npm': {
        'n8n': {},
    },
    'n8n': {
        'DB_TYPE': 'postgresdb',
        'DB_POSTGRESDB_DATABASE': 'n8n',
        'DB_POSTGRESDB_HOST': 'localhost',
        'DB_POSTGRESDB_PORT': 5432,
        'DB_POSTGRESDB_USER': 'n8n',
        'DB_POSTGRESDB_PASSWORD': database_password,
    },
    'postgresql': {
        'databases': {
            'n8n': {
                'when_creating': {
                    'encoding': 'UTF8',
                    'collation': 'C.UTF-8',
                    'ctype': 'C.UTF-8',
                },
                'owner': 'n8n',
            },
        },
        'roles': {
            'n8n': {
                'password': database_password,
            },
        },
    },
    'systemd': {
        'units': {
            'n8n.service': {
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
                    'Environment': {
                        'NODE_ENV=production',
                    },
                },
            },
        },
    },
    'users': {
        'n8n': {
            'home': '/opt/n8n',
        },
    },
    'zfs': {
        'datasets': {
            'tank/n8n': {
                'mountpoint': '/opt/n8n',
                'needed_by': {'directory:/opt/n8n'},
            },
        },
    },
}


@metadata_reactor.provides(
    'systemd/services/n8n.service',
)
def systemd(metadata):
    return {
        'systemd': {
            'units': {
                'n8n.service': {
                    'Service': {
                        'Environment': metadata.get('n8n'),
                    },
                },
            },
        },
    }
