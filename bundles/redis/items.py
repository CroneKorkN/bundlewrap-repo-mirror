directories = {
    '/etc/redis': {
        'purge': True,
        'owner': 'redis',
        'mode': '2770',
        'needs': [
            'pkg_apt:redis-server',
        ],
    },
    '/var/lib/redis': {
        'owner': 'redis',
        'group': 'redis',
        'mode': '0750',
        'needs': [
            'pkg_apt:redis-server',
        ],
    },
}

files = {
    '/etc/systemd/system/redis.service': {
        'delete': True,
        'needs': [
            'pkg_apt:redis-server',
        ],
    },
}

svc_systemd = {
    'redis': {
        'running': False,
        'enabled': False,
        'needs': [
            'pkg_apt:redis-server',
        ],
    },
}

for name, conf in node.metadata.get('redis').items():
    files[f'/etc/redis/{name}.conf'] = {
        'content': '\n'.join(
            f'{key} {value}'
                for key, values in sorted(conf.items())
                for value in ([values] if isinstance(values, str) else sorted(values))
                if value is not False
        ) + '\n',
        'owner': 'redis',
        'triggers': [
            f'svc_systemd:redis-{name}:restart'
        ],
    }

    svc_systemd[f'redis-{name}'] = {
        'needs': [
            'svc_systemd:redis',
            f'file:/etc/redis/{name}.conf',
        ],
    }
