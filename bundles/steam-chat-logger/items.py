src = '/opt/steam_chat_logger/src'
home = '/var/lib/steam_chat_logger'

directories = {
    '/opt/steam_chat_logger': {},
    # git_deploy needs its target to exist
    src: {},
    home: {
        'owner': 'steam_chat_logger',
        'mode': '0755',
        'needs': [
            'zfs_dataset:tank/steam-chat-logger'
        ],
    },
    f'{home}/steamuserimages': {
        'owner': 'steam_chat_logger',
        'mode': '0755',
        'needs': [
            'zfs_dataset:tank/steam-chat-logger'
        ],
    },
    # avatars/<hash>_full.jpg, nginx serves them to the viewer
    f'{home}/avatars': {
        'owner': 'steam_chat_logger',
        'mode': '0755',
        'needs': [
            'zfs_dataset:tank/steam-chat-logger'
        ],
    },
}

files = {
    # left from the checkout before src/
    '/opt/steam_chat_logger/steam_chat_logger.py': {
        'delete': True,
    },
    # left from the logger's own steam logins; the browser userscript delivers the chats now
    '/usr/local/bin/steam-chat-logger-login': {
        'delete': True,
    },
    f'{home}/refresh_token': {
        'delete': True,
    },
    f'{home}/oauth_token': {
        'delete': True,
    },
}

git_deploy = {
    src: {
        'repo': 'https://git.sublimity.de/cronekorkn/steam_chat_logger.git',
        'rev': 'master',
        'triggers': [
            'action:steam_chat_logger_uv_sync',
        ],
    },
}

actions = {
    'steam_chat_logger_uv_sync': {
        # the venv lives in the user's home, the checkout stays root-owned
        'command': (
            f'cd {home} && sudo -u steam_chat_logger env HOME={home} UV_PROJECT_ENVIRONMENT={home}/.venv '
            f'/usr/local/bin/uv sync --frozen --project {src}'
        ),
        'triggered': True,
        'cascade_skip': False,
        'triggers': [
            'svc_systemd:steam-chat-logger.service:restart',
        ],
        'needs': [
            f'git_deploy:{src}',
            'action:install_uv',
            f'directory:{home}',
            'user:steam_chat_logger',
        ],
    },
}


# TODO
'''
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    checksum VARCHAR(64) UNIQUE NOT NULL,
    from_url VARCHAR(255) NOT NULL,
    from_name VARCHAR(255) NOT NULL,
    to_url VARCHAR(255) NOT NULL,
    to_name VARCHAR(255) NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    message TEXT NOT NULL
)
'''
