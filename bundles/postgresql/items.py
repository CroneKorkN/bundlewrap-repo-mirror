pkg_apt = {
    'postgresql': {},
}

if node.has_bundle('zfs'):
    pkg_apt[postgresql]\
        .setdefault('needs', [])\
        .append('zfs_dataset:tank/postgresql')

for user, config in node.metadata.get('postgresql/roles').items():
    postgres_roles[user] = {
        'password': config['password'],
        'needs': {
            'svc_systemd:postgresql',
        },
    }

for database, config in node.metadata.get('postgresql/databases').items():
    postgres_dbs[database] = config

svc_systemd = {
    'postgresql': {},
}
