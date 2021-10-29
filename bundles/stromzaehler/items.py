influxdb_metadata = repo.get_node(node.metadata.get('stromzaehler/influxdb_node')).metadata.get('influxdb')

files = {
    '/opt/stromzaehler': {
        'content_type': 'mako',
        'mode': '550',
        'context': {
            'node_name': node.name,
            'influxdb_domain': influxdb_metadata['hostname'],
            'influxdb_bucket': influxdb_metadata['bucket'],
            'influxdb_org': influxdb_metadata['org'],
            'influxdb_token': influxdb_metadata['admin_token'],
        },
        'triggers': [
            'svc_systemd:stromzaehler:restart'
        ],
    },
}

svc_systemd = {
    'stromzaehler': {
        # 'enabled': False,
        # 'running': False,
        'needs': [
            'pkg_apt:gpiod',
            'file:/opt/stromzaehler',
        ],
    }
}
