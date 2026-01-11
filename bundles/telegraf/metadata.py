h = repo.libs.hashable.hashable

defaults = {
    'apt': {
        'packages': {
            'telegraf': {},
            # needed by crystal plugins:
            'libgc-dev': {},
            'libevent-dev': {},
        },
        'sources': {
            'influxdata': {
                'urls': {
                    'https://repos.influxdata.com/debian',
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
    'telegraf': {
        'agent': {
            'hostname': node.name,
            'collection_jitter': '20s',
            'flush_interval': '20s',
            'flush_jitter': '5s',
            'interval': '2m',
            'metric_batch_size': 1000,
            'metric_buffer_limit': 10000,
            'omit_hostname': False,
            'round_interval': True,
            'skip_processors_after_aggregators': True,
        },
        'inputs': {
            'cpu': {
                'default': {
                    'collect_cpu_time': False,
                    'percpu': True,
                    'report_active': False,
                    'totalcpu': True,
                },
            },
            'disk': {
                'default': {
                    'ignore_fs': [
                        'tmpfs',
                        'devtmpfs',
                        'devfs',
                        'iso9660',
                        'overlay',
                        'aufs',
                        'squashfs',
                    ],
                }
            },
            'procstat': {
                'default': {
                    'interval': '60s',
                    'pattern': '.',
                    'fieldinclude': [
                        'cpu_usage',
                        'memory_rss',
                    ],
                },
            },
            'diskio': {
                'default': {
                    'device_tags': ["ID_PART_ENTRY_NUMBER"],
                }
            },
            'kernel': {
                'default': {},
            },
            'mem': {
                'default': {},
            },
            'processes': {
                'default': {},
            },
            'swap': {
                'default': {},
            },
            'system': {
                'default': {},
            },
            'net': {
                'default': {},
            },
            'exec': {
                # h({
                #     'commands': [
                #         f'sudo /usr/local/share/telegraf/procio',
                #     ],
                #     'data_format': 'influx',
                #     'interval': '20s',
                # }),
                'pressure_stall': {
                    'commands': [
                        f'/usr/local/share/telegraf/pressure_stall',
                    ],
                    'data_format': 'influx',
                    'interval': '10s',
                },
            },
        },
        'processors': {},
        'outputs': {},
    },
    'grafana_rows': {
        'cpu',
        'mem',
        'disk_io',
        'disk_usage',
        'net_io',
        'proc_cpu_ram',
        'proc_io',
    },
    'sudoers': {
        'telegraf': {'/usr/local/share/telegraf/procio'},
    },
}


@metadata_reactor.provides(
    'telegraf/outputs/influxdb_v2/default',
)
def influxdb(metadata):
    influxdb_metadata = repo.get_node(metadata.get('telegraf/influxdb_node')).metadata.get('influxdb')

    return {
        'telegraf': {
            'outputs': {
                'influxdb_v2': {
                    'default': {
                        'urls': [f"http://{influxdb_metadata['hostname']}:{influxdb_metadata['port']}"],
                        'token': str(influxdb_metadata['writeonly_token']),
                        'organization': influxdb_metadata['org'],
                        'bucket': influxdb_metadata['bucket'],
                    },
                },
            },
        },
    }


# crystal based (procio, pressure_stall):
@metadata_reactor.provides(
    'apt/packages/libpcre2-8-0',
    'apt/packages/libpcre3',
)
def libpcre(metadata):
    if node.os == 'debian' and node.os_version >= (13,):
        libpcre_package = 'libpcre2-8-0'
    else:
        libpcre_package = 'libpcre3'

    return {
        'apt': {
            'packages': {
                libpcre_package: {},
            },
        },
    }
