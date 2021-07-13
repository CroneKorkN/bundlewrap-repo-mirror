version = version=node.metadata.get('gitea/version')

downloads['/usr/local/bin/gitea'] = {
    'url': f'https://dl.gitea.io/gitea/{version}/gitea-{version}-linux-amd64',
    'sha256': node.metadata.get('gitea/sha256'),
    'triggers': {
        'svc_systemd:gitea:restart',
    },
    'preceded_by': {
        'action:stop_gitea',
    },
}

users['git'] = {}

directories['/var/lib/gitea'] = {
    'owner': 'git',
    'mode': '0700',
    'triggers': {
        'svc_systemd:gitea:restart',
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

files['/etc/gitea/app.ini'] = {
    'content_type': 'mako',
    'owner': 'git',
    'context': node.metadata['gitea'],
    'triggers': {
        'svc_systemd:gitea:restart',
    },
}

svc_systemd['gitea'] = {
    'needs': {
        'action:chmod_gitea',
        'download:/usr/local/bin/gitea',
        'file:/etc/gitea/app.ini',
    },
}
