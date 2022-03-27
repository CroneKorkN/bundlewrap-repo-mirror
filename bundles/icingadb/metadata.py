defaults = {
    'apt': {
        'packages': {
            'icingadb': {},
            'icingadb-redis': {},
            'icingadb-web': {},
        },
        'sources': {
            'deb https://packages.icinga.com/debian icinga-{release} main',
            'deb https://packages.icinga.com/debian icinga-{release}-snapshots main',
        },
    },
    'postgresql': {
        'databases': {
            'icingadb': {
                'owner': 'icingadb',
            },
        },
        'roles': {
            'icingadb': {
                'password': repo.vault.password_for(f'psql icingadb on {node.name}'),
            },
        },
    },
    'redis': {
        'icingadb': {
            'port': '6381',
        },
    },
}

@metadata_reactor.provides(
    'icingadb',
)
def config(metadata):
    return {
        'icingadb': {
            'database': {
                'type': 'postgresql',
                'host': 'localhost',
                'port': 3306,
                'database': 'icingadb',
                'user': 'icingadb',
                'password': metadata.get('postgresql/roles/icingadb/password'),
            },
            'redis': {
                'address': 'localhost:6380',
            },
            'logging': {
                'level': 'info',
            },
        },
    }
