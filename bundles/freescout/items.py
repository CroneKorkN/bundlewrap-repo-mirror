# https://github.com/freescout-helpdesk/freescout/wiki/Installation-Guide
run_as = repo.libs.tools.run_as
php_version = node.metadata.get('php/version')


directories = {
    '/opt/freescout': {
        'owner': 'www-data',
        'group': 'www-data',
        # chown -R www-data:www-data /opt/freescout
    },
}

actions = {
    'clone_freescout': {
        'command': run_as('www-data', 'git clone https://github.com/freescout-helpdesk/freescout.git /opt/freescout'),
        'unless': 'test -e /opt/freescout/.git',
        'needs': [
            'pkg_apt:git',
            'directory:/opt/freescout',
        ],
    },
    'pull_freescout': {
        'command': run_as('www-data', 'git -C /opt/freescout pull'),
        'unless': run_as('www-data', 'git -C /opt/freescout fetch origin && git -C /opt/freescout status -uno | grep -q "Your branch is up to date"'),
        'needs': [
            'action:clone_freescout',
        ],
        'triggers': [
            'action:freescout_artisan_update',
            f'svc_systemd:php{php_version}-fpm.service:restart',
        ],
    },
    'freescout_artisan_update': {
        'command': run_as('www-data', 'php /opt/freescout/artisan freescout:after-app-update'),
        'triggered': True,
        'needs': [
            f'svc_systemd:php{php_version}-fpm.service:restart',
            'action:pull_freescout',
        ],
    },
}

# files = {
#     '/opt/freescout/.env': {
#         'content': '\n'.join(
#             f'{k}={v}' for k, v in
#                 sorted(node.metadata.get('freescout/env').items())
#         ),
#         'needs': [
#             'directory:/opt/freescout',
#             'action:clone_freescout',
#         ],
#     },
# }
