from shlex import quote

directories = {
    '/var/lib/mysql': {
        'owner': 'mysql',
        'group': 'mysql',
        'needs': [
            'zfs_dataset:tank/mariadb',
        ],
        'needed_by': [
            'pkg_apt:mariadb-server',
        ],
    },
}

files = {
    '/etc/mysql/conf.d/override.conf': {
        'context': {
            'conf': node.metadata.get('mariadb/conf'),
        },
        'content_type': 'mako',
    },
}

svc_systemd = {
    'mariadb.service': {
        'needs': [
            'pkg_apt:mariadb-server',
        ],
    },
}

for db, conf in node.metadata.get('mariadb/databases', {}).items():
    actions[f'mariadb_create_database_{db}'] = {
        'command': 'mariadb -Bsr --execute ' + quote(f"CREATE DATABASE {db}"),
        'unless': '! mariadb -Bsr --execute ' + quote(f"SHOW DATABASES LIKE '{db}'") + ' | grep -q ^db$',
        'needs': [
            'svc_systemd:mariadb.service',
        ],
    }
