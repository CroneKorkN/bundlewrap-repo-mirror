h = repo.libs.hashable.hashable

defaults = {
    'apt': {
        'packages': {
            'telegraf': {},
        },
    },
    'telegraf': {
        'config': {
            'agent': {
                'hostname': node.name,
                'collection_jitter': '0s',
                'flush_interval': '15s',
                'flush_jitter': '0s',
                'interval': '15s',
                'metric_batch_size': 1000,
                'metric_buffer_limit': 10000,
                'omit_hostname': False,
                'round_interval': True,
            },
            'inputs': {
                'cpu': {h({
                    'collect_cpu_time': False,
                    'percpu': True,
                    'report_active': False,
                    'totalcpu': True,
                })},
                'disk': {h({
                    'ignore_fs': [
                        'tmpfs',
                        'devtmpfs',
                        'devfs',
                        'iso9660',
                        'overlay',
                        'aufs',
                        'squashfs',
                    ],
                })},
                'procstat': {h({
                    'interval': '60s',
                    'pattern': '.',
                    'fieldpass': [
                        'cpu_usage',
                        'memory_rss',
                    ],
                })},
                'diskio': {h({})},
                'kernel': {h({})},
                'mem': {h({})},
                'processes': {h({})},
                'swap': {h({})},
                'system': {h({})},
                'net': {h({})},
                'exec': {h({
                    'commands': [
                        f'sudo /usr/local/share/telegraf/procio',
                    ],
                    'data_format': 'influx',
                    'interval': '20s',
                })},
            },
        },
    },
    'grafana_rows': {
        'cpu',
        'mem',
        'disk_io',
        'disk_usage',
        'net_io',
        'proc_cpu',
        'proc_ram',
        'proc_io',
    },
    'sudoers': {
        'telegraf': {'/usr/local/share/telegraf/procio'},
    },
}


@metadata_reactor.provides(
    'apt/sources',
)
def apt(metadata):
    release = {
        'buster': 'buster',
        'bullseye': 'bullseye',
        'bookworm': 'bullseye',
    }[metadata.get('os_release')]

    return {
        'apt': {
            'packages': {
                'telegraf': {},
            },
            'sources': {
                f"deb https://repos.influxdata.com/debian {release} stable",
            },
        },
    }


@metadata_reactor.provides(
    'telegraf/config/outputs/influxdb_v2',
)
def influxdb(metadata):
    influxdb_metadata = repo.get_node(metadata.get('telegraf/influxdb_node')).metadata.get('influxdb')

    return {
        'telegraf': {
            'config': {
                'outputs': {
                    'influxdb_v2': [{
                        'urls': [f"http://{influxdb_metadata['hostname']}:{influxdb_metadata['port']}"],
                        'token': str(influxdb_metadata['writeonly_token']),
                        'organization': influxdb_metadata['org'],
                        'bucket': influxdb_metadata['bucket'],
                    }]
                },
            },
        },
    }
