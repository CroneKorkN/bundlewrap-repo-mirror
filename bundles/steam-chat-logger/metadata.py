defaults = {
    'postgresql': {
        'roles': {
            'steam_chat_logger': {
                'password': repo.vault.password_for(f'{node.name} postgresql steam_chat_logger'),
            },
        },
        'databases': {
            'steam_chat_logger': {
                'owner': 'steam_chat_logger',
            },
        },
    },
    'users': {
        'steam_chat_logger': {},
    },
    'zfs': {
        'datasets': {
            'tank/steam-chat-logger': {
                'mountpoint': '/var/lib/steam_chat_logger',
            },
        },
    },
}


@metadata_reactor.provides(
    'systemd-timers/steam-chat-logger',
)
def systemd_timer(metadata):
    return {
        'systemd-timers': {
            'steam-chat-logger': {
                'command': '/var/lib/steam_chat_logger/.venv/bin/python /opt/steam_chat_logger/src/steam_chat_logger.py',
                'when': 'hourly',
                'user': 'steam_chat_logger',
                'env': {
                    'DB_NAME': 'steam_chat_logger',
                    'DB_USER': 'steam_chat_logger',
                    'DB_PASSWORD': metadata.get('postgresql/roles/steam_chat_logger/password'),
                },
                'working_dir': '/var/lib/steam_chat_logger',
            },
        },
    }
