defaults = {
    'apt': {
        'packages': {
            'mariadb-server': {
                'needs': {
                    'zfs_dataset:tank/mariadb',
                },
            },
            'mariadb-client': {
                'needs': {
                    'zfs_dataset:tank/mariadb',
                },
            },
        },
    },
    'mariadb': {
        'databases': {},
        'conf': {
            # https://www.reddit.com/r/zfs/comments/u1xklc/mariadbmysql_database_settings_for_zfs
            'mysqld': {
                'skip-innodb_doublewrite': None,
                'innodb_flush_method': 'fsync',
                'innodb_doublewrite': '0',
                'innodb_use_atomic_writes': '0',
                'innodb_use_native_aio': '0',
                'innodb_read_io_threads': '10',
                'innodb_write_io_threads': '10',
                'innodb_buffer_pool_size': '26G',
                'innodb_flush_log_at_trx_commit': '1',
                'innodb_log_file_size': '1G',
                'innodb_flush_neighbors': '0',
                'innodb_fast_shutdown': '2',
            },
        },
    },
    'zfs': {
        'datasets': {
            'tank/mariadb': {
                'mountpoint': '/var/lib/mysql',
                'recordsize': '16384',
                'atime': 'off',
            },
        },
    },
}
