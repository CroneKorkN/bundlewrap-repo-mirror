from tomlkit import dumps
from shlex import quote

directories['/var/lib/influxdb'] = {
    'owner': 'influxdb',
    'group': 'influxdb',
    'mode': '0750',
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

actions['wait_for_influxdb_start'] = {
    'command': 'sleep 15',
    'triggered': True,
    'triggered_by': [
        'svc_systemd:influxdb',
        'svc_systemd:influxdb:restart',
    ]
}

actions['setup_influxdb'] = {
    'command': 'influx setup --username={username} --password={password} --org={org} --bucket={bucket} --token={token} --retention=0 --force'.format(
        username=node.metadata.get('influxdb/username'),
        password=quote(str(node.metadata.get('influxdb/password'))),
        org=node.metadata.get('influxdb/org'),
        bucket=node.metadata.get('influxdb/bucket'),
        token=str(node.metadata.get('influxdb/admin_token')),
    ),
    'unless': 'influx bucket list',
    'needs': [
        'action:wait_for_influxdb_start',
    ],
}

files['/root/.influxdbv2/configs'] = {
    'content': dumps({
        node.metadata.get('influxdb/bucket'): {
            'url': f"http://localhost:{node.metadata.get('influxdb/port')}",
            'token': str(node.metadata.get('influxdb/admin_token')),
            'org': node.metadata.get('influxdb/org'),
            'active': True,
        },
    }),
    'needs': [
        'action:setup_influxdb',
    ],
}

for description, permissions in {
    'readonly': '--read-buckets',
    'writeonly': '--write-buckets --read-telegrafs',
}.items():
    actions[f'influxdb_{description}_token'] = {
        'command': f'influx auth create --description {description} {permissions}',
        'unless': f'''influx auth list --json | jq -r '.[] | select (.description == "{description}") | .token' | wc -l | grep -q ^1$''',
        'needs': [
            'file:/root/.influxdbv2/configs',
        ],
    }
