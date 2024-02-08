version = node.metadata.get('php/version')

files = {
    f'/etc/php/{version}/cli/php.ini': {
        'content': repo.libs.ini.dumps(node.metadata.get('php/php.ini')),
        'needs': {
            f'pkg_apt:php{version}',
            f'pkg_apt:php{version}-fpm',
        },
    },
    f'/etc/php/{version}/fpm/php.ini': {
        'content': repo.libs.ini.dumps(node.metadata.get('php/php.ini')),
        'needs': {
            f'pkg_apt:php{version}',
            f'pkg_apt:php{version}-fpm',
        },
        'triggers': {
            f'svc_systemd:php{version}-fpm.service:restart',
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
            f'svc_systemd:php{version}-fpm.service:restart',
        },
    },
}

svc_systemd = {
    f'php{version}-fpm.service': {
        'needs': {
            'pkg_apt:',
            f'file:/etc/php/{version}/fpm/php.ini',
        },
    },
}
