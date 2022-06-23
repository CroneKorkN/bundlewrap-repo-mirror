from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'influxdb2': {},
            'influxdb2-cli': {},
        },
        'sources': {
            'deb https://repos.influxdata.com/debian {release} stable',
        },
    },
    'influxdb': {
        'port': '8200',
        'username': 'admin',
        'org': 'default',
        'bucket': 'default',
        'config': {
            'bolt-path': '/var/lib/influxdb/influxd.bolt',
            'engine-path': '/var/lib/influxdb/engine',
            'reporting-disabled': True,
            'http-bind-address': ':8200',
        },
    },
}

@metadata_reactor.provides(
    'influxdb/password',
    'influxdb/admin_token',
)
def admin_password(metadata):
    return {
        'influxdb': {
            'password': repo.vault.password_for(f"{metadata.get('id')} influxdb admin"),
            'admin_token': repo.vault.random_bytes_as_base64_for(f"{metadata.get('id')} influxdb default token", length=64),
        },
    }


@metadata_reactor.provides(
    'zfs/datasets',
)
def zfs(metadata):
    if not node.has_bundle('zfs'):
        return {}

    return {
        'zfs': {
            'datasets': {
                f"{metadata.get('zfs/storage_classes/ssd')}/influxdb": {
                    'mountpoint': '/var/lib/influxdb',
                    'recordsize': '8192',
                    'atime': 'off',
                },
            },
        },
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    return {
        'dns': {
            metadata.get('influxdb/hostname'): repo.libs.dns.get_a_records(metadata),
        }
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('influxdb/hostname'): {
                    'content': 'nginx/proxy_pass.conf',
                    'context': {
                        'target': 'http://127.0.0.1:8200',
                    }
                },
            },
        },
    }
