defaults = {
    'steam-chat-logger': {
        'import_port': 4002,
        'import_token': repo.vault.password_for(f'{node.name} steam-chat-logger import'),
    },
    'monitoring': {
        'services': {
            # the userscript delivers once a day and steam keeps about 14 days: 4 days leave time to react
            'steam chat import': {
                'vars.command': "/bin/sh -c 'find /var/lib/steam_chat_logger/last_import -mtime -4 | grep -q . || exit 2'",
            },
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
    'systemd': {
        'services': {
            'steam-chat-logger.service': {
                'needs': [
                    'action:steam_chat_logger_uv_sync',
                    'postgres_db:steam_chat_logger',
                ],
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
    'systemd/units/steam-chat-logger.service',
)
def receiver(metadata):
    return {
        'systemd': {
            'units': {
                'steam-chat-logger.service': {
                    'Unit': {
                        'Description': 'receives steam chat exports from the browser userscript',
                        'After': 'network.target',
                    },
                    'Service': {
                        'Environment': {
                            'DB_NAME=steam_chat_logger',
                            'DB_USER=steam_chat_logger',
                            f"DB_PASSWORD={metadata.get('postgresql/roles/steam_chat_logger/password')}",
                            f"IMPORT_PORT={metadata.get('steam-chat-logger/import_port')}",
                            f"IMPORT_TOKEN={metadata.get('steam-chat-logger/import_token')}",
                        },
                        'User': 'steam_chat_logger',
                        'WorkingDirectory': '/var/lib/steam_chat_logger',
                        'ExecStart': '/var/lib/steam_chat_logger/.venv/bin/python /opt/steam_chat_logger/src/receiver.py',
                        'Restart': 'on-failure',
                    },
                },
            },
        },
    }
