defaults = {
    'apt': {
        'packages': {
            'redis-server': {},
        },
    },
    'backup': {
        'paths': {
            '/var/lib/redis',
        },
    },
    'redis': {
        'server': {},
    },
}

if node.has_bundle('zfs'):
    defaults['zfs'] = {
        'datasets': {
            'tank/redis': {
                'mountpoint': '/var/lib/redis',
                'needed_by': [
                    'pkg_apt:redis-server',
                    'directory:/var/lib/redis',
                ],
            },
        },
    }


@metadata_reactor.provides(
    'redis',
)
def config(metadata):
    redis = {}
    
    for name, conf in metadata.get('redis').items():
        redis[name] = {
            'bind': '127.0.0.1 ::1',
            'protected-mode': 'yes',
            'port': '6379',
            'tcp-backlog': '511',
            'unixsocket': f'/var/run/redis-{name}/redis.sock',
            'unixsocketperm': '700',
            'timeout': '0',
            'tcp-keepalive': '300',
            'daemonize': 'yes',
            'supervised': 'no',
            'pidfile': f'/var/run/redis-{name}/redis.pid',
            'loglevel': 'notice',
            'logfile': f'/var/log/redis/{name}.log',
            'databases': '16',
            'always-show-logo': 'yes',
            'save': '900 1',
            'save': '300 10',
            'save': '60 10000',
            'stop-writes-on-bgsave-error': 'yes',
            'rdbcompression': 'yes',
            'rdbchecksum': 'yes',
            'dbfilename': f'{name}.rdb',
            'dir': '/var/lib/redis',
            'replica-serve-stale-data': 'yes',
            'replica-read-only': 'yes',
            'repl-diskless-sync': 'no',
            'repl-diskless-sync-delay': '5',
            'repl-disable-tcp-nodelay': 'no',
            'replica-priority': '100',
            'lazyfree-lazy-eviction': 'no',
            'lazyfree-lazy-expire': 'no',
            'lazyfree-lazy-server-del': 'no',
            'replica-lazy-flush': 'no',
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
            'client-output-buffer-limit': 'normal 0 0 0',
            'client-output-buffer-limit': 'replica 256mb 64mb 60',
            'client-output-buffer-limit': 'pubsub 32mb 8mb 60',
            'hz': '10',
            'dynamic-hz': 'yes',
            'aof-rewrite-incremental-fsync': 'yes',
            'rdb-save-incremental-fsync': 'yes',
        }
    
    return {
        'redis': redis,
    }


@metadata_reactor.provides(
    'systemd/units',
)
def units(metadata):
    units = {}
    
    for name, conf in metadata.get('redis').items():
        units[f'redis-{name}.service'] = {
            'Unit': {
                'Description': f'redis {name}',
                'After': 'network.target',
            },
            'Service': {
                'Type': 'notify',
                'ExecStart': f'/usr/bin/redis-server /etc/redis/{name}.conf --supervised systemd --daemonize no',
                'PIDFile': f'/run/redis-{name}/redis.pid',
                'TimeoutStopSec': '0',
                'Restart': 'always',
                'User': 'redis',
                'Group': 'redis',
                'RuntimeDirectory': f'redis-{name}',
                'RuntimeDirectoryMode': '2755',
                
                'UMask': '007',
                'PrivateTmp': 'yes',
                'LimitNOFILE': '65535',
                'PrivateDevices': 'yes',
                'ProtectHome': 'yes',
                'ReadOnlyDirectories': '/',
                'ReadWritePaths': [
                    '-/var/lib/redis',
                    '-/var/log/redis',
                    f'-/var/run/redis-{name}',
                ],
                
                'NoNewPrivileges': 'true',
                'CapabilityBoundingSet': 'CAP_SETGID CAP_SETUID CAP_SYS_RESOURCE',
                'MemoryDenyWriteExecute': 'true',
                'ProtectKernelModules': 'true',
                'ProtectKernelTunables': 'true',
                'ProtectControlGroups': 'true',
                'RestrictRealtime': 'true',
                'RestrictNamespaces': 'true',
                'RestrictAddressFamilies': 'AF_INET AF_INET6 AF_UNIX',
                
                'ProtectSystem': 'true',
            },
            'Install': {
                'WantedBy': {'multi-user.target'},
                'Alias': f'redis-{name}.service',
            },
        }
    
    return {
        'systemd': {
            'units': units,
        }
    }
