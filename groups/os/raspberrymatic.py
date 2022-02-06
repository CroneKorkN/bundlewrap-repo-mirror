{
    'supergroups': [
        'all',
    ],
    'bundles': [
        'users',
    ],
    'metadata': {
        'users': {
            'root': {
                'password': None,
                'shell': '/bin/sh',
                'ssh_dir': '/usr/local/etc/ssh',
            },
        },
        'hostname_file': '/var/etc/hostname',
    },
    'cmd_wrapper_outer': 'sh -c {}',
    'cmd_wrapper_inner': '{}',
    'lock_dir': '/tmp/bundlewrap',
}
