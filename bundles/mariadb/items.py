from shlex import quote

def mariadb(sql, **kwargs):
    kwargs_string = ''.join(f" --{k} {v}" for k, v in kwargs.items())
    return f"mariadb{kwargs_string} -Bsr --execute {quote(sql)}"

directories = {
    '/var/lib/mysql': {
        'owner': 'mysql',
        'group': 'mysql',
        'needs': [
            'zfs_dataset:tank/mariadb',
        ],
        'needs': [
            'pkg_apt:mariadb-server',
            'pkg_apt:mariadb-client',
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
            'pkg_apt:mariadb-client',
        ],
    },
}

actions = {
    'mariadb_sec_remove_anonymous_users': {
        'command': mariadb("DELETE FROM mysql.global_priv WHERE User=''"),
        'unless': mariadb("SELECT count(0) FROM mysql.global_priv WHERE User = ''") + " | grep -q '^0$'",
        'needs': [
            'svc_systemd:mariadb.service',
        ],
        'triggers': [
            'svc_systemd:mariadb.service:restart',
        ],
    },
    'mariadb_sec_remove_remote_root': {
        'command': mariadb("DELETE FROM mysql.global_priv WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')"),
        'unless': mariadb("SELECT count(0) FROM mysql.global_priv WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1')") + " | grep -q '^0$'",
        'needs': [
            'svc_systemd:mariadb.service',
        ],
        'triggers': [
            'svc_systemd:mariadb.service:restart',
        ],
    },
}

for db, conf in node.metadata.get('mariadb/databases', {}).items():
    actions[f'mariadb_create_database_{db}'] = {
        'command': mariadb(f"CREATE DATABASE {db}"),
        'unless': mariadb(f"SHOW DATABASES LIKE '{db}'") + f" | grep -q '^{db}$'",
        'needs': [
            'svc_systemd:mariadb.service',
        ],
    }
    actions[f'mariadb_user_{db}_create'] = {
        'command': mariadb(f"CREATE USER {db}"),
        'unless': mariadb(f"SELECT User FROM mysql.user WHERE User = '{db}'") + f" | grep -q '^{db}$'",
        'needs': [
            f'action:mariadb_create_database_{db}',
        ],
    }
    pw = conf['password']
    actions[f'mariadb_user_{db}_password'] = {
        'command': mariadb(f"SET PASSWORD FOR {db} = PASSWORD('{conf['password']}')"),
        'unless': f'echo {quote(pw)} | mariadb -u {db} -e quit -p',
        'needs': [
            f'action:mariadb_user_{db}_create',
        ],
    }
    actions[f'mariadb_grant_privileges_to_{db}'] = {
        'command': mariadb(f"GRANT ALL PRIVILEGES ON {db}.* TO '{db}'", database=db),
        'unless': mariadb(f"SHOW GRANTS FOR {db}") + f" | grep -q '^GRANT ALL PRIVILEGES ON `{db}`.* TO `{db}`@`%`'",
        'needs': [
            f'action:mariadb_user_{db}_create',
        ],
    }
