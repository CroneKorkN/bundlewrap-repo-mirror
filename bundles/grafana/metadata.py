from mako.template import Template

postgres_password = repo.vault.password_for(f'{node.name} postgres role grafana')

defaults = {
    'apt': {
        'packages': {
            'grafana': {},
        },
        'sources': {
            'grafana': {
                'urls': {
                    'https://packages.grafana.com/oss/deb',
                },
                'suites': {
                    'stable',
                },
                'components': {
                    'main',
                },
            },
        },

    },
    'grafana': {
        'config': {
            'server': {
                'http_port': 8300,
            },
            'database': {
                'url': f'postgres://grafana:{postgres_password}@localhost:5432/grafana',
            },
            'remote_cache': {
                'type': 'redis',
                'connstr': 'addr=127.0.0.1:6379',
            },
            'security': {
                'admin_user': 'admin',
                'admin_password': str(repo.vault.password_for(f'{node.name} grafana admin')),
            },
            'users': {
                'allow_signup': False,
            },
        },
        'datasources': {},
    },
    'postgresql': {
        'databases': {
            'grafana': {
                'owner': 'grafana',
            },
        },
        'roles': {
            'grafana': {
                'password': postgres_password,
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/grafana': {
                'mountpoint': '/var/lib/grafana'
            },
        },
    },
}


@metadata_reactor.provides(
    'grafana/config/server/domain',
)
def domain(metadata):
    return {
        'grafana': {
            'config': {
                'server': {
                    'domain': metadata.get('grafana/hostname'),
                },
            },
        },
    }

@metadata_reactor.provides(
    'grafana/datasources',
)
def influxdb2(metadata):
    influxdb_metadata = repo.get_node(metadata.get('grafana/influxdb_node')).metadata.get('influxdb')

    return {
        'grafana': {
            'datasources': {
                f"influxdb@{influxdb_metadata['hostname']}": {
                    'type': 'influxdb',
                    'url': f"http://{influxdb_metadata['hostname']}:{influxdb_metadata['port']}",
                    'jsonData': {
                        'version': 'Flux',
                        'organization': influxdb_metadata['org'],
                        'defaultBucket': influxdb_metadata['bucket'],
                    },
                    'secureJsonData': {
                        'token': str(influxdb_metadata['readonly_token']),
                    },
                    'editable': False,
                    'isDefault': True,
                },
            },
        },
    }


@metadata_reactor.provides(
    'grafana/datasources',
)
def datasource_key_to_name(metadata):
    return {
        'grafana': {
            'datasources': {
                name: {'name': name} for name in metadata.get('grafana/datasources').keys()
            },
        },
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('grafana/hostname'): repo.libs.ip.get_a_records(metadata),
        }
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('grafana/hostname'): {
                    'content': 'grafana/vhost.conf',
                },
            },
        },
    }
