users = {
    'steam': {
        'home': '/opt/steam',
    },
}

directories = {
    '/opt/steam': {
        'owner': 'steam',
        'group': 'steam',
    },
}

files = {
    '/opt/steam/steamcmd_linux.tar.gz': {
        'content_type': 'download',
        'source': 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz',
        'owner': 'steam',
        'group': 'steam',
    },
}

actions = {
    'extract_steamcmd': {
        'command': 'tar xfvz /opt/steam/steamcmd_linux.tar.gz --directory /opt/steam',
        'unless': 'test -f /opt/steam/steamcmd.sh',
        'needs': [
            'file:/opt/steam/steamcmd_linux.tar.gz',
        ],
    },
    'chown_steamcmd': {
        'command': 'chown -R steam:steam /opt/steam',
        'triggered': True,
        'triggered_by': [
            'action:extract_steamcmd',
        ],
    },
}

# sudo -Hiu steam bash -c '~/steam/steamcmd.sh +login anonymous +force_install_dir ./l4d2/ +app_update 222860 validate +quit'
# https://github.com/SegoCode/swd/releases/download/1.1/swd-linux-amd64
