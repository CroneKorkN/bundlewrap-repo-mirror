{
    'hostname': '10.0.0.2',
    'groups': [
        'archive',
        'backup',
        'debian-10',
#        'nextcloud',
    ],
    'bundles': [
        'gitea',
        'grafana',
        'influxdb2',
        'postgresql',
        'wireguard',
        'zfs',
    ],
    'metadata': {
        'id': 'af96709e-b13f-4965-a588-ef2cd476437a',
        'network': {
            'internal': {
                'interface': 'enp1s0f0',
                'ipv4': '10.0.0.2/24',
                'gateway4': '10.0.0.1',
            },
        },
        'gitea': {
            'version': '1.14.2',
            'sha256': '0d11d87ce60d5d98e22fc52f2c8c6ba2b54b14f9c26c767a46bf102c381ad128',
            'domain': 'git.sublimity.de',
        },
        'grafana': {
            'hostname': 'grafana.sublimity.de',
        },
        'influxdb': {
            'hostname': 'influxdb.sublimity.de',
            'client_token': '!decrypt:encrypt$gAAAAABg25z8fEYjuRkhg4XuYMtJsPO5SaqlexuricXPZAzZ51_iQtPe5v7S503hMFdZ7j-XQUP6Q2y3ovbzhouRYeRZy1W020csOOtBcH08X-ya9cCAOCMnJdujg0MVakxPJhNPa5Ip5XsI4Bjb0EcftNDayQWQsZw1vFHBHllD-ALTisoCdbImD6a1iT4NuT57JGydbWGW',
        },
        'users': {
            'root': {
                'shell': '/usr/bin/zsh',
            },
        },
        'wireguard': {
            'my_ip': '172.30.0.2/24',
            'peers': {
                'htz.mails': {
                    'route': [
                        '10.0.10.0/24',
                        '10.0.11.0/24',
                    ],
                },
            },
        },
        'zfs': {
            'pools': {
                'tank': {
                    'mirrors': [
                        '/dev/disk/by-partlabel/zfs-data-1',
                        '/dev/disk/by-partlabel/zfs-data-2',
                    ],
                },
            },
        },
    },
}
