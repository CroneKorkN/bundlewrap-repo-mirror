defaults = {
    'apt': {
        'packages': {
            'python3-pip': {},
        },
    },
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
        # steam python login is broken: https://github.com/ValvePython/steam/issues/442
        # 'systemd-timers': {
        #     f'steam-chat-logger': {
        #         'command': '/opt/steam_chat_logger/steam_chat_logger.py',
        #         'when': 'hourly',
        #         'user': 'steam_chat_logger',
        #         'env': {
        #             'DB_NAME': 'steam_chat_logger',
        #             'DB_USER': 'steam_chat_logger',
        #             'DB_PASSWORD': metadata.get('postgresql/roles/steam_chat_logger/password'),
        #             **metadata.get('steam_chat_logger'),
        #         },
        #         'working_dir': '/var/lib/steam_chat_logger',
        #     },
        # },
    }
