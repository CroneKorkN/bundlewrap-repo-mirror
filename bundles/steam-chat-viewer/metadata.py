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
    # the database belongs to steam-chat-logger; declared here too so the viewer works while the logger is paused
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
                        # the receiver of steam-chat-logger, where the node has that bundle
                        'import_port': metadata.get('steam-chat-logger/import_port', None),
                    },
                },
            },
        },
    }
