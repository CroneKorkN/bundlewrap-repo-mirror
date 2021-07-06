from bundlewrap.utils.dicts import merge_dict


svc_systemd['postgresql'] = {
    'needs': [
        'pkg_apt:postgresql',
    ],
}

for user, config in node.metadata.get('postgresql/roles').items():
    postgres_roles[user] = merge_dict(config, {
        'needs': [
            'svc_systemd:postgresql',
        ],
    })

for database, config in node.metadata.get('postgresql/databases').items():
    postgres_dbs[database] = merge_dict(config, {
        'needs': [
            'svc_systemd:postgresql',
        ],
    })