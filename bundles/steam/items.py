users = {
    'steam': {
        'home': '/opt/steam/steam',
    },
}

directories = {
    '/opt/steam': {
        'owner': 'steam',
        'group': 'steam',
        'needs': [
            'zfs_dataset:tank/steam',
        ],
    },
    '/opt/steam/steam': {
        'owner': 'steam',
        'group': 'steam',
    },
}
for game in node.metadata.get('steam/games'):
    directories[f'/opt/steam/{game}'] = {
        'owner': 'steam',
        'group': 'steam',
        'needed_by': [
            'svc_systemd:steam-update',
        ],
    }

files = {
    '/opt/steam/steam/steamcmd_linux.tar.gz': {
        'content_type': 'download',
        'source': 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz',
        'owner': 'steam',
        'group': 'steam',
    },
    '/opt/steam/steam/workshop-downloader': {
        'content_type': 'download',
        'source': 'https://github.com/SegoCode/swd/releases/download/1.1/swd-linux-amd64',
        'owner': 'steam',
        'group': 'steam',
        'mode': '750',
    },
}

# symlinks = {
#     # /opt/steam/.steam/sdk32/steamclient.so: cannot open shared object file: No such file or directory
#     '/opt/steam/.steam/sdk32': {
#         'target': '/opt/steam/linux32',
#     }
# }

actions = {
    'extract_steamcmd': {
        'command': """su - steam -c 'tar xfvz /opt/steam/steam/steamcmd_linux.tar.gz --directory /opt/steam/steam'""",
        'unless': 'test -f /opt/steam/steam/steamcmd.sh',
        'needs': [
            'file:/opt/steam/steam/steamcmd_linux.tar.gz',
        ],
    },
}

svc_systemd['steam-update'] = {
    'running': False,
    'enabled': False,
    'needs': {
        'file:/usr/local/lib/systemd/system/steam-update.service',
    }
}
