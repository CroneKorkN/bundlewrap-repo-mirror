from ipaddress import ip_interface

defaults = {
    'flask': {
        'steam-chat-viewer' : {
            'git_url': "https://git.sublimity.de/cronekorkn/steam-chat-viewer.git",
            'port': 4001,
            'app_module': 'steam_chat_viewer',
            'user': 'steam_chat_viewer',
            'group': 'steam_chat_viewer',
            'timeout': 900,
            'env': {
                'DB_HOST': 'localhost',
                'DB_NAME': 'steam_chat_logger',
                'DB_USER': 'steam_chat_logger',
            },
        },
    },
    'users': {
        'steam_chat_viewer': {},
    },
}


@metadata_reactor.provides(
    'flask/steam-chat-viewer/env/DB_PASSWORD',
)
def agent_conf(metadata):
    return {
        'flask': {
            'steam-chat-viewer': {
                'env': {
                    'DB_PASSWORD': metadata.get('postgresql/roles/steam_chat_logger/password'),
                },
            },
        },
    }


@metadata_reactor.provides(
    'nginx/vhosts',
)
def nginx(metadata):
    return {
        'nginx': {
            'vhosts': {
                metadata.get('steam-chat-viewer/hostname'): {
                    'content': 'steam-chat-viewer/vhost.conf',
                    'context': {
                        'target': 'http://127.0.0.1:4001',
                    },
                },
            },
        },
    }
