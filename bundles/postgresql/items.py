from bundlewrap.utils.dicts import merge_dict


version = node.metadata.get('postgresql/version')

directories = {
    '/var/lib/postgresql': {
        'owner': 'postgres',
        'group': 'postgres',
        'needs': [
            'pkg_apt:postgresql',
            'zfs_dataset:tank/postgresql',
        ],
        'needed_by': [
            'svc_systemd:postgresql.service',
        ],
    }
}

files = {
    f"/etc/postgresql/{version}/main/conf.d/managed.conf": {
        'content': '\n'.join(
            f'{key} = {value}'
                for key, value in sorted(node.metadata.get('postgresql/conf').items())
        ) + '\n',
        'owner': 'postgres',
        'group': 'postgres',
        'needs': [
            'pkg_apt:postgresql',
        ],
        'needed_by': [
            'svc_systemd:postgresql.service',
        ],
        'triggers': [
            'svc_systemd:postgresql.service:restart',
        ],
    },
}

svc_systemd['postgresql.service'] = {
    'needs': [
        'pkg_apt:postgresql',
    ],
}

for user, config in node.metadata.get('postgresql/roles').items():
    postgres_roles[user] = merge_dict(config, {
        'needs': [
            'svc_systemd:postgresql.service',
        ],
    })

for database, config in node.metadata.get('postgresql/databases').items():
    postgres_dbs[database] = merge_dict(config, {
        'needs': [
            'svc_systemd:postgresql.service',
        ],
    })
