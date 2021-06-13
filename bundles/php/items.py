version = node.metadata.get('php/version')

php_ini_context = {
    'num_cpus': node.metadata.get('vm/cpu'),
    'post_max_size': node.metadata.get('php/post_max_size', 10),
}

files = {
    f'/etc/php/{version}/fpm/php.ini': {
        'content_type': 'mako',
        'context': php_ini_context,
        'needs': {
            # "all php packages"
            'pkg_apt:'
        },
        'triggers': {
            f'svc_systemd:php{version}-fpm:restart',
        },
    },
    f'/etc/php/{version}/cli/php.ini': {
        'content_type': 'mako',
        'context': php_ini_context,
        'needs': {
            # "all php packages"
            'pkg_apt:'
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
