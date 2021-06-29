from tomlkit import dumps
from shlex import quote

directories['/var/lib/influxdb'] = {
    'owner': 'influxdb',
    'group': 'influxdb',
    'needs': [
        'zfs_dataset:tank/influxdb',
    ],
}

directories['/etc/influxdb'] = {
    'purge': True,
}
files['/etc/influxdb/config.toml'] = {
    'content': dumps(node.metadata.get('influxdb/config')),
    'triggers': [
        'svc_systemd:influxdb:restart',
    ]
}

svc_systemd['influxdb'] = {
    'needs': [
        'directory:/var/lib/influxdb',
        'file:/etc/influxdb/config.toml',
        'pkg_apt:influxdb2',
    ]
}

actions['setup_influxdb'] = {
    'command': 'influx setup --username={username} --password={password} --org={org} --bucket={bucket} --token={token} --retention=0 --force'.format(
        username=node.metadata.get('influxdb/username'),
        password=quote(str(node.metadata.get('influxdb/password'))),
        org=node.metadata.get('influxdb/org'),
        bucket=node.metadata.get('influxdb/bucket'),
        token=str(node.metadata.get('influxdb/token')),
    ),
    'unless': 'influx bucket list',
    'needs': [
        'svc_systemd:influxdb',
    ],
}

files['/root/.influxdbv2/configs'] = {
    'content': dumps({
        node.metadata.get('influxdb/bucket'): {
            'url': f"http://localhost:{node.metadata.get('influxdb/port')}",
            'token': str(node.metadata.get('influxdb/token')),
            'org': node.metadata.get('influxdb/org'),
            'active': True,
        },
    }),
    'needs': [
        'action:setup_influxdb',
    ],
}
