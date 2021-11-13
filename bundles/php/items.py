version = node.metadata.get('php/version')

php_ini_context = {
    'num_cpus': node.metadata.get('vm/cores'),
    'post_max_size': node.metadata.get('php/post_max_size'),
}

files = {
    f'/etc/php/{version}/cli/php.ini': {
        'content_type': 'mako',
        'context': php_ini_context,
        'needs': {
            f'pkg_apt:php{version}',
            f'pkg_apt:php{version}-fpm',
        },
    },
    f'/etc/php/{version}/fpm/php.ini': {
        'content_type': 'mako',
        'context': php_ini_context,
        'needs': {
            f'pkg_apt:php{version}',
            f'pkg_apt:php{version}-fpm',
        },
        'triggers': {
            f'svc_systemd:php{version}-fpm:restart',
        },
    },
    f'/etc/php/{version}/fpm/pool.d/www.conf': {
        'content': repo.libs.ini.dumps({
            'www': node.metadata.get('php/www.conf'),
        }),
        'needs': {
            f'pkg_apt:php{version}',
            f'pkg_apt:php{version}-fpm',
        },
        'triggers': {
            f'svc_systemd:php{version}-fpm:restart',
        },
    },
}

svc_systemd = {
    f'php{version}-fpm': {
        'needs': {
            'pkg_apt:',
            f'file:/etc/php/{version}/fpm/php.ini',
        },
    },
}
