downloads = {
    '/usr/local/bin/gitea': {
        'url': 'https://dl.gitea.io/gitea/{version}/gitea-{version}-linux-amd64'.format(version=node.metadata['gitea']['version']),
        'sha256': node.metadata['gitea']['sha256'],
        'triggers': {
            'svc_systemd:gitea:restart',
        },
        'preceded_by': {
            'action:stop_gitea',
        },
    },
}

users = {
    'gitea': {},
}

directories = {
    '/var/lib/gitea': {
        'owner': 'gitea',
        'mode': '0700',
        'triggers': {
            'svc_systemd:gitea:restart',
        },
    },
}

actions = {
    'chmod_gitea': {
        'command': 'chmod a+x /usr/local/bin/gitea',
        'unless': 'test -x /usr/local/bin/gitea',
        'needs': {
            'download:/usr/local/bin/gitea',
        },
    },
    'stop_gitea': {
        'command': 'systemctl stop gitea',
        'triggered': True,
    },
}

files = {
    '/etc/gitea/app.ini': {
        'content_type': 'mako',
        'context': node.metadata['gitea'],
        'triggers': {
            'svc_systemd:gitea:restart',
        },
    },
}
