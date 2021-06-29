from ipaddress import ip_interface

defaults = {
    'apt': {
        'packages': {
            'influxdb2': {},
        },
        'sources': [
            'deb https://repos.influxdata.com/debian {release} stable',
        ],
    },
    'influxdb': {
        'port': '8200',
        'username': 'admin',
        'org': 'default',
        'org': 'default',
        'bucket': 'default',
        'config': {
            'bolt-path': '/var/lib/influxdb/influxd.bolt',
            'engine-path': '/var/lib/influxdb/engine',
            'reporting-disabled': True,
            'http-bind-address': ':8200'
        },
    },
    'zfs': {
        'datasets': {
            'tank/influxdb': {
                'mountpoint': '/var/lib/influxdb'
            },
        },
    },
}

@metadata_reactor.provides(
    'influxdb/password',
)
def admin_password(metadata):
    return {
        'influxdb': {
            'password': repo.vault.password_for(f"{node.metadata.get('id')} influxdb admin"),
            'token': repo.vault.random_bytes_as_base64_for(f"{node.metadata.get('id')} influxdb default token", length=64),
        },
    }


@metadata_reactor.provides(
    'dns',
)
def dns(metadata):
    dns = {}
    
    dns[metadata.get('influxdb/hostname')] = {
        'A': [
            str(ip_interface(network['ipv4']).ip)
                for network in metadata.get('network').values()
                if 'ipv4' in network
        ],
        'AAAA': [
            str(ip_interface(network['ipv6']).ip)
                for network in metadata.get('network').values()
                if 'ipv6' in network
        ],
    }

    return {
        'dns': dns,
    }
