defaults = {
    'apt': {
        'packages': {
            'telegraf': {},
        },
        'sources': [
            'deb https://repos.influxdata.com/debian {release} stable',
        ],
    },
    'telegraf': {
        'config': {
            'agent': {
                'hostname': node.name,
                'collection_jitter': '0s',
                'flush_interval': '10s',
                'flush_jitter': '0s',
                'interval': '10s',
                'metric_batch_size': 1000,
                'metric_buffer_limit': 10000,
                'omit_hostname': False,
                'round_interval': True
            },
            'inputs': {
                'cpu': [{
                    'collect_cpu_time': False,
                    'percpu': True,
                    'report_active': False,
                    'totalcpu': True
                }],
                'disk': [{
                    'ignore_fs': [
                        'tmpfs',
                        'devtmpfs',
                        'devfs',
                        'iso9660',
                        'overlay',
                        'aufs',
                        'squashfs'
                    ],
                }],
                'diskio': [{}],
                'kernel': [{}],
                'mem': [{}],
                'processes': [{}],
                'swap': [{}],
                'system': [{}],
            },
        },
    },
}


@metadata_reactor.provides(
    'telegraf/config/outputs/influxdb_v2',
)
def influxdb(metadata):
    influxdb_node = repo.get_node(metadata.get('telegraf/influxdb_node'))

    influxdb_server_url = "http://{hostname}:{port}".format(
        hostname=influxdb_node.metadata.get('influxdb/hostname'),
        port=influxdb_node.metadata.get('influxdb/port'),
    )

    return {
        'telegraf': {
            'config': {
                'outputs': {
                    'influxdb_v2': [{
                        'urls': [influxdb_server_url],
                        'token': str(influxdb_node.metadata.get('influxdb/token')),
                        'organization': influxdb_node.metadata.get('influxdb/org'),
                        'bucket': influxdb_node.metadata.get('influxdb/bucket'),
                    }]
                },
            },
        },
    }
