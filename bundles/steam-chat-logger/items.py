directories = {
    '/opt/steam_chat_logger': {
        'owner': 'steam_chat_logger',
    },
    '/var/lib/steam_chat_logger': {
        'owner': 'steam_chat_logger',
        'mode': '0770',
        'needs': [
            'zfs_dataset:tank/steam-chat-logger'
        ],
    },
}

git_deploy = {
    '/opt/steam_chat_logger': {
        'repo': 'https://git.sublimity.de/cronekorkn/steam_chat_logger.git',
        'rev': 'master',
    }
}

pkg_pip = {
    'steam': {},
    'beautifulsoup4': {},
    'pytz': {},
    'pg8000': {},
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
