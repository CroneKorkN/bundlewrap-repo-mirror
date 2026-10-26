# one instance of debian's redis-server@.service per client, each a key in the redis metadata with its overrides.
# a client reaches its instance on /run/redis-<name>/redis-server.sock and joins the redis group,
# see the nextcloud and rspamd bundles.

# the unit passes --supervised systemd --daemonize no; paths per instance follow below
CONFIG = {
    'bind': '127.0.0.1 -::1',
    'protected-mode': 'yes',
    'port': '0',
    'tcp-backlog': '511',
    'unixsocketperm': '770',
    'timeout': '0',
    'tcp-keepalive': '300',
    'loglevel': 'notice',
    'databases': '16',
    'always-show-logo': 'no',
    'save': {
        '900 1',
        '300 10',
        '60 10000',
    },
    'stop-writes-on-bgsave-error': 'yes',
    'rdbcompression': 'yes',
    'rdbchecksum': 'yes',
    'lazyfree-lazy-eviction': 'no',
    'lazyfree-lazy-expire': 'no',
    'lazyfree-lazy-server-del': 'no',
    'appendonly': 'no',
    'appendfilename': '"appendonly.aof"',
    'appendfsync': 'everysec',
    'no-appendfsync-on-rewrite': 'no',
    'auto-aof-rewrite-percentage': '100',
    'auto-aof-rewrite-min-size': '64mb',
    'aof-load-truncated': 'yes',
    'aof-use-rdb-preamble': 'yes',
    'lua-time-limit': '5000',
    'slowlog-log-slower-than': '10000',
    'slowlog-max-len': '128',
    'latency-monitor-threshold': '0',
    'notify-keyspace-events': '""',
    'hash-max-ziplist-entries': '512',
    'hash-max-ziplist-value': '64',
    'list-max-ziplist-size': '-2',
    'list-compress-depth': '0',
    'set-max-intset-entries': '512',
    'zset-max-ziplist-entries': '128',
    'zset-max-ziplist-value': '64',
    'hll-sparse-max-bytes': '3000',
    'stream-node-max-bytes': '4096',
    'stream-node-max-entries': '100',
    'activerehashing': 'yes',
    'client-output-buffer-limit': {
        'normal 0 0 0',
        'pubsub 32mb 8mb 60',
    },
    'hz': '10',
    'dynamic-hz': 'yes',
    'aof-rewrite-incremental-fsync': 'yes',
    'rdb-save-incremental-fsync': 'yes',
}

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

files = {}

svc_systemd = {
    # the unnamed instance has no client
    'redis-server': {
        'running': False,
        'enabled': False,
        'masked': True,
        'needs': [
            'pkg_apt:redis-server',
        ],
    },
}

for name, overrides in node.metadata.get('redis').items():
    config = {
        **CONFIG,
        # paths the template unit expects or allows
        'unixsocket': f'/run/redis-{name}/redis-server.sock',
        'pidfile': f'/run/redis-{name}/redis-server.pid',
        'logfile': f'/var/log/redis/redis-server-{name}.log',
        'dir': f'/var/lib/redis/{name}',
        'dbfilename': 'dump.rdb',
        **overrides,
    }

    directories[f'/var/lib/redis/{name}'] = {
        'owner': 'redis',
        'group': 'redis',
        'mode': '0750',
    }

    files[f'/etc/redis/redis-{name}.conf'] = {
        'content': '\n'.join(
            f'{key} {value}'
                for key, values in sorted(config.items())
                for value in ([values] if isinstance(values, str) else sorted(values))
                if value is not False
        ) + '\n',
        'owner': 'redis',
        'triggers': [
            f'svc_systemd:redis-server@{name}:restart',
        ],
    }

    svc_systemd[f'redis-server@{name}'] = {
        'needs': [
            f'file:/etc/redis/redis-{name}.conf',
            f'directory:/var/lib/redis/{name}',
            'svc_systemd:redis-server',
        ],
    }
